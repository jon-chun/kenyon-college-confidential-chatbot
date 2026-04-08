"""Unit tests for scraper module — no network access."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.kenyon_bot.config import ScrapeTarget
from src.kenyon_bot.scraper import scrape_single, scrape_targets


@pytest.fixture
def target():
    return ScrapeTarget(
        filename="test-page.md",
        url="https://www.kenyon.edu/test/",
        category="departments",
    )


class TestScrapeSingle:
    """Tests for scrape_single with mocked crawler."""

    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self, target):
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.markdown = "# Test Page\n\nLots of content here " * 10
        mock_result.error_message = None

        crawler = AsyncMock()
        crawler.arun = AsyncMock(return_value=mock_result)

        result = await scrape_single(crawler, target, timeout=10, max_retries=1)
        assert result.success
        assert result.attempts == 1
        assert result.char_count > 100

    @pytest.mark.asyncio
    async def test_failure_with_empty_content(self, target):
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.markdown = ""
        mock_result.error_message = None

        crawler = AsyncMock()
        crawler.arun = AsyncMock(return_value=mock_result)

        result = await scrape_single(crawler, target, timeout=10, max_retries=1, backoff_base=0.01)
        assert not result.success
        assert "Empty" in result.error or "short" in result.error

    @pytest.mark.asyncio
    async def test_failure_with_too_short_content(self, target):
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.markdown = "tiny"
        mock_result.error_message = None

        crawler = AsyncMock()
        crawler.arun = AsyncMock(return_value=mock_result)

        result = await scrape_single(crawler, target, timeout=10, max_retries=1, backoff_base=0.01)
        assert not result.success

    @pytest.mark.asyncio
    async def test_retries_on_failure(self, target):
        mock_result = MagicMock()
        mock_result.success = False
        mock_result.markdown = ""
        mock_result.error_message = "Server error"

        crawler = AsyncMock()
        crawler.arun = AsyncMock(return_value=mock_result)

        result = await scrape_single(crawler, target, timeout=10, max_retries=3, backoff_base=0.01)
        assert not result.success
        assert result.attempts == 3
        assert crawler.arun.call_count == 3

    @pytest.mark.asyncio
    async def test_succeeds_on_retry(self, target):
        fail_result = MagicMock()
        fail_result.success = False
        fail_result.markdown = ""
        fail_result.error_message = "Temporary error"

        success_result = MagicMock()
        success_result.success = True
        success_result.markdown = "# Success\n" * 20
        success_result.error_message = None

        crawler = AsyncMock()
        crawler.arun = AsyncMock(side_effect=[fail_result, success_result])

        result = await scrape_single(crawler, target, timeout=10, max_retries=3, backoff_base=0.01)
        assert result.success
        assert result.attempts == 2

    @pytest.mark.asyncio
    async def test_timeout_handling(self, target):
        crawler = AsyncMock()
        crawler.arun = AsyncMock(side_effect=asyncio.TimeoutError())

        result = await scrape_single(crawler, target, timeout=1, max_retries=2, backoff_base=0.01)
        assert not result.success
        assert "Timeout" in result.error

    @pytest.mark.asyncio
    async def test_exception_handling(self, target):
        crawler = AsyncMock()
        crawler.arun = AsyncMock(side_effect=ConnectionError("Network down"))

        result = await scrape_single(crawler, target, timeout=10, max_retries=1, backoff_base=0.01)
        assert not result.success
        assert "Network down" in result.error

    @pytest.mark.asyncio
    async def test_result_contains_target(self, target):
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.markdown = "x" * 200
        mock_result.error_message = None

        crawler = AsyncMock()
        crawler.arun = AsyncMock(return_value=mock_result)

        result = await scrape_single(crawler, target, timeout=10, max_retries=1)
        assert result.target is target
        assert result.target.filename == "test-page.md"


class TestScrapeTargets:
    """Tests for scrape_targets with mocked crawler."""

    @pytest.mark.asyncio
    async def test_scrapes_all_targets(self, tmp_path):
        targets = [
            ScrapeTarget(filename="a.md", url="https://example.com/a", category="departments"),
            ScrapeTarget(filename="b.md", url="https://example.com/b", category="research"),
        ]

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.markdown = "# Page Content\n" * 20
        mock_result.error_message = None

        with patch("src.kenyon_bot.scraper.AsyncWebCrawler") as MockCrawler:
            instance = AsyncMock()
            instance.arun = AsyncMock(return_value=mock_result)
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockCrawler.return_value = instance

            report = await scrape_targets(
                targets=targets,
                max_concurrent=2,
                delay=0.01,
                vault_root=tmp_path,
            )

        assert report.total == 2
        assert report.succeeded == 2

    @pytest.mark.asyncio
    async def test_saves_files_to_vault(self, tmp_path):
        targets = [
            ScrapeTarget(
                filename="dept.md", url="https://example.com/dept", category="departments"
            ),
        ]

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.markdown = "# Department Content Here\n" * 20
        mock_result.error_message = None

        with patch("src.kenyon_bot.scraper.AsyncWebCrawler") as MockCrawler:
            instance = AsyncMock()
            instance.arun = AsyncMock(return_value=mock_result)
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockCrawler.return_value = instance

            await scrape_targets(
                targets=targets,
                max_concurrent=1,
                delay=0.01,
                vault_root=tmp_path,
            )

        saved = tmp_path / "00-Raw-Sources" / "dept.md"
        assert saved.exists()
        assert len(saved.read_text()) > 100

    @pytest.mark.asyncio
    async def test_empty_targets_list(self, tmp_path):
        report = await scrape_targets(
            targets=[],
            max_concurrent=1,
            delay=0.01,
            vault_root=tmp_path,
        )
        assert report.total == 0

    @pytest.mark.asyncio
    async def test_report_tracks_failures(self, tmp_path):
        targets = [
            ScrapeTarget(
                filename="fail.md", url="https://example.com/fail", category="departments"
            ),
        ]

        mock_result = MagicMock()
        mock_result.success = False
        mock_result.markdown = ""
        mock_result.error_message = "Server error"

        with patch("src.kenyon_bot.scraper.AsyncWebCrawler") as MockCrawler:
            instance = AsyncMock()
            instance.arun = AsyncMock(return_value=mock_result)
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockCrawler.return_value = instance

            report = await scrape_targets(
                targets=targets,
                max_concurrent=1,
                delay=0.01,
                vault_root=tmp_path,
            )

        assert report.failed == 1
        assert len(report.failures) == 1
