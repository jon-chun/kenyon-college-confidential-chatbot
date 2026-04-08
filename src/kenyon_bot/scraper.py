"""Kenyon.edu web scraper with parallel execution and retry logic."""

import asyncio
import logging
import time
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

from .config import (
    ALL_TARGETS,
    MAX_CONCURRENT_SCRAPERS,
    MAX_RETRIES,
    REQUEST_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_BACKOFF_BASE,
    ScrapeReport,
    ScrapeResult,
    ScrapeTarget,
)
from .vault import save_scraped_content

logger = logging.getLogger(__name__)


def _extract_content(result: object) -> str:
    """Extract the best Markdown content from a crawl4ai result.

    Tries fit_markdown (cleaner) first, then falls back to raw markdown.
    Handles cases where attributes may not exist or may not be strings.
    """
    # Try markdown_v2.fit_markdown first
    try:
        md_v2 = getattr(result, "markdown_v2", None)
        if md_v2 is not None:
            fit = getattr(md_v2, "fit_markdown", None)
            if isinstance(fit, str) and len(fit.strip()) > 50:
                return fit
    except (TypeError, AttributeError):
        pass

    # Fall back to raw markdown
    raw = getattr(result, "markdown", None)
    if isinstance(raw, str):
        return raw

    return ""


async def scrape_single(
    crawler: AsyncWebCrawler,
    target: ScrapeTarget,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
    max_retries: int = MAX_RETRIES,
    backoff_base: float = RETRY_BACKOFF_BASE,
) -> ScrapeResult:
    """Scrape a single URL with retry and exponential backoff.

    Returns a ScrapeResult with success/failure details.
    """
    last_error = ""
    for attempt in range(1, max_retries + 1):
        try:
            # On first attempt, filter aggressively for clean content.
            # On retries, relax filters to handle JS-heavy pages.
            if attempt == 1:
                config = CrawlerRunConfig(
                    word_count_threshold=10,
                    excluded_tags=["nav", "footer", "header", "script", "style"],
                    exclude_external_links=True,
                    wait_until="networkidle",
                    page_timeout=timeout * 1000,
                )
            else:
                config = CrawlerRunConfig(
                    word_count_threshold=5,
                    wait_until="networkidle",
                    page_timeout=timeout * 1000,
                )

            result = await asyncio.wait_for(
                crawler.arun(url=target.url, config=config),
                timeout=timeout + 10,
            )

            # Try fit_markdown first (cleaner), fall back to markdown
            content = _extract_content(result)

            if result.success and content and len(content.strip()) > 100:
                return ScrapeResult(
                    target=target,
                    success=True,
                    markdown=content,
                    char_count=len(content),
                    attempts=attempt,
                )

            last_error = getattr(result, "error_message", None) or "Empty or too-short content"
            logger.warning(
                "Attempt %d/%d failed for %s: %s",
                attempt,
                max_retries,
                target.filename,
                last_error,
            )

        except asyncio.TimeoutError:
            last_error = f"Timeout after {timeout}s"
            logger.warning(
                "Attempt %d/%d timed out for %s",
                attempt,
                max_retries,
                target.filename,
            )
        except Exception as exc:
            last_error = str(exc)
            logger.warning(
                "Attempt %d/%d error for %s: %s",
                attempt,
                max_retries,
                target.filename,
                last_error,
            )

        if attempt < max_retries:
            backoff = backoff_base**attempt
            logger.info("Backing off %.1fs before retry...", backoff)
            await asyncio.sleep(backoff)

    return ScrapeResult(
        target=target,
        success=False,
        error=last_error,
        attempts=max_retries,
    )


async def _worker(
    name: str,
    crawler: AsyncWebCrawler,
    queue: asyncio.Queue[ScrapeTarget],
    results: list[ScrapeResult],
    delay: float,
    vault_root: Path | None,
) -> None:
    """Worker coroutine that pulls targets from the queue and scrapes them."""
    while True:
        try:
            target = queue.get_nowait()
        except asyncio.QueueEmpty:
            break

        logger.info("[%s] Scraping %s → %s", name, target.filename, target.url)
        result = await scrape_single(crawler, target)
        results.append(result)

        if result.success:
            save_scraped_content(target.filename, result.markdown, root=vault_root)
            logger.info(
                "[%s] ✓ %s — %d chars (attempt %d)",
                name,
                target.filename,
                result.char_count,
                result.attempts,
            )
        else:
            logger.error(
                "[%s] ✗ %s — %s (after %d attempts)",
                name,
                target.filename,
                result.error,
                result.attempts,
            )

        # Polite delay between requests
        await asyncio.sleep(delay)
        queue.task_done()


async def scrape_targets(
    targets: list[ScrapeTarget] | None = None,
    max_concurrent: int = MAX_CONCURRENT_SCRAPERS,
    delay: float = REQUEST_DELAY_SECONDS,
    vault_root: Path | None = None,
) -> ScrapeReport:
    """Scrape multiple targets with parallel workers and rate limiting.

    Args:
        targets: List of ScrapeTarget to scrape (defaults to ALL_TARGETS).
        max_concurrent: Maximum number of parallel browser workers.
        delay: Seconds to wait between requests per worker.
        vault_root: Override vault root directory for saving files.

    Returns:
        ScrapeReport summarizing all results.
    """
    targets = targets if targets is not None else ALL_TARGETS
    report = ScrapeReport()

    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
    )

    queue: asyncio.Queue[ScrapeTarget] = asyncio.Queue()
    for target in targets:
        await queue.put(target)

    results: list[ScrapeResult] = []

    async with AsyncWebCrawler(config=browser_config) as crawler:
        workers = [
            _worker(
                name=f"worker-{i}",
                crawler=crawler,
                queue=queue,
                results=results,
                delay=delay,
                vault_root=vault_root,
            )
            for i in range(min(max_concurrent, len(targets)))
        ]
        await asyncio.gather(*workers)

    report.results = results
    return report


async def scrape_all(vault_root: Path | None = None) -> ScrapeReport:
    """Convenience wrapper: scrape all configured targets into the vault."""
    from .vault import create_vault

    root = create_vault(vault_root)
    logger.info("Scraping %d targets into %s", len(ALL_TARGETS), root)

    start = time.monotonic()
    report = await scrape_targets(vault_root=root)
    elapsed = time.monotonic() - start

    logger.info(
        "Scraping complete: %d/%d succeeded, %d failed, %d total chars in %.1fs",
        report.succeeded,
        report.total,
        report.failed,
        report.total_chars,
        elapsed,
    )

    if report.failures:
        logger.warning("Failed targets:")
        for r in report.failures:
            logger.warning("  - %s: %s", r.target.filename, r.error)

    return report
