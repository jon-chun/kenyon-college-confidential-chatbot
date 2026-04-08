"""Integration tests that hit live kenyon.edu — marked slow."""

import pytest
from crawl4ai import AsyncWebCrawler, BrowserConfig

from src.kenyon_bot.config import CORE_TARGETS, ScrapeTarget
from src.kenyon_bot.scraper import scrape_single, scrape_targets
from src.kenyon_bot.vault import create_vault, get_raw_source_files, validate_vault


@pytest.mark.slow
@pytest.mark.integration
class TestLiveSingleScrape:
    """Test scraping individual pages from kenyon.edu."""

    @pytest.fixture
    async def crawler(self):
        config = BrowserConfig(headless=True, verbose=False)
        async with AsyncWebCrawler(config=config) as c:
            yield c

    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    async def test_scrape_departments_page(self, crawler):
        target = ScrapeTarget(
            filename="departments.md",
            url="https://www.kenyon.edu/academics/departments-and-majors/",
            category="departments",
        )
        result = await scrape_single(crawler, target, timeout=30)
        assert result.success, f"Failed to scrape departments: {result.error}"
        assert result.char_count > 500, "Departments page seems too short"
        assert "biology" in result.markdown.lower() or "Biology" in result.markdown

    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    async def test_scrape_research_page(self, crawler):
        target = ScrapeTarget(
            filename="research.md",
            url="https://www.kenyon.edu/academics/student-research/",
            category="research",
        )
        result = await scrape_single(crawler, target, timeout=30)
        assert result.success, f"Failed to scrape research: {result.error}"
        assert result.char_count > 200

    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    async def test_scrape_catalog_page(self, crawler):
        target = ScrapeTarget(
            filename="catalog.md",
            url="https://www.kenyon.edu/offices-and-services/registrar/kenyon-college-course-catalog/",
            category="courses",
        )
        result = await scrape_single(crawler, target, timeout=30)
        assert result.success, f"Failed to scrape catalog: {result.error}"
        assert result.char_count > 200

    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    async def test_scrape_returns_markdown_not_html(self, crawler):
        target = ScrapeTarget(
            filename="departments.md",
            url="https://www.kenyon.edu/academics/departments-and-majors/",
            category="departments",
        )
        result = await scrape_single(crawler, target, timeout=30)
        assert result.success
        # Should be Markdown, not raw HTML
        assert "<html>" not in result.markdown.lower()
        assert "<body>" not in result.markdown.lower()

    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    async def test_scrape_invalid_url_fails_gracefully(self, crawler):
        target = ScrapeTarget(
            filename="nonexistent.md",
            url="https://www.kenyon.edu/this-page-does-not-exist-404/",
            category="departments",
        )
        result = await scrape_single(crawler, target, timeout=15, max_retries=1)
        # Should either fail or return very short content (404 page)
        # The key is it doesn't crash
        assert isinstance(result.success, bool)


@pytest.mark.slow
@pytest.mark.integration
class TestLiveBatchScrape:
    """Test batch scraping with multiple targets."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(120)
    async def test_scrape_core_targets(self, tmp_path):
        """Scrape the 5 core targets — the minimum viable dataset."""
        vault = create_vault(tmp_path / "vault")

        report = await scrape_targets(
            targets=CORE_TARGETS,
            max_concurrent=2,
            delay=2.0,
            vault_root=vault,
        )

        assert report.total == len(CORE_TARGETS)
        # Allow some failures (network issues) but most should succeed
        assert report.succeeded >= 3, (
            f"Too many failures: {report.failed}/{report.total}. "
            f"Failures: {[(r.target.filename, r.error) for r in report.failures]}"
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(120)
    async def test_scraped_files_saved_to_vault(self, tmp_path):
        vault = create_vault(tmp_path / "vault")

        # Scrape just 2 targets for speed
        targets = CORE_TARGETS[:2]
        report = await scrape_targets(
            targets=targets,
            max_concurrent=2,
            delay=2.0,
            vault_root=vault,
        )

        files = get_raw_source_files(vault)
        assert len(files) == report.succeeded, "Saved file count doesn't match success count"

        for f in files:
            content = f.read_text()
            assert len(content) > 100, f"{f.name} is suspiciously short ({len(content)} chars)"

    @pytest.mark.asyncio
    @pytest.mark.timeout(120)
    async def test_vault_valid_after_scrape(self, tmp_path):
        vault = create_vault(tmp_path / "vault")

        await scrape_targets(
            targets=CORE_TARGETS[:2],
            max_concurrent=2,
            delay=2.0,
            vault_root=vault,
        )

        issues = validate_vault(vault)
        assert issues == [], f"Vault invalid after scrape: {issues}"
