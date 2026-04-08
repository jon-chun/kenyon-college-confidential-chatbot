"""Unit tests for config module."""

import pytest

from src.kenyon_bot.config import (
    ALL_TARGETS,
    BASE_URL,
    CORE_TARGETS,
    DEPARTMENT_TARGETS,
    MAX_CONCURRENT_SCRAPERS,
    MAX_RETRIES,
    REQUEST_DELAY_SECONDS,
    RESOURCE_TARGETS,
    ScrapeReport,
    ScrapeResult,
    ScrapeTarget,
)


class TestScrapeTarget:
    """Tests for ScrapeTarget dataclass."""

    def test_creation(self):
        target = ScrapeTarget(
            filename="test.md",
            url="https://example.com",
            category="departments",
        )
        assert target.filename == "test.md"
        assert target.url == "https://example.com"
        assert target.category == "departments"

    def test_is_frozen(self):
        target = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        with pytest.raises(AttributeError):
            target.filename = "other.md"  # type: ignore[misc]

    def test_equality(self):
        a = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        b = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        assert a == b

    def test_hash(self):
        target = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        assert hash(target) == hash(target)
        s = {target}
        assert target in s


class TestScrapeResult:
    """Tests for ScrapeResult dataclass."""

    def test_default_values(self):
        target = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        result = ScrapeResult(target=target, success=True)
        assert result.markdown == ""
        assert result.error == ""
        assert result.char_count == 0
        assert result.attempts == 1

    def test_success_result(self):
        target = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        markdown = "# Test\nContent here"
        result = ScrapeResult(
            target=target,
            success=True,
            markdown=markdown,
            char_count=len(markdown),
            attempts=1,
        )
        assert result.success
        assert len(result.markdown) == 19
        assert result.char_count == len(result.markdown)

    def test_failure_result(self):
        target = ScrapeTarget(filename="test.md", url="https://example.com", category="test")
        result = ScrapeResult(
            target=target,
            success=False,
            error="Timeout",
            attempts=3,
        )
        assert not result.success
        assert result.error == "Timeout"
        assert result.attempts == 3


class TestScrapeReport:
    """Tests for ScrapeReport dataclass."""

    @pytest.fixture
    def _target(self):
        return ScrapeTarget(filename="test.md", url="https://example.com", category="test")

    def test_empty_report(self):
        report = ScrapeReport()
        assert report.total == 0
        assert report.succeeded == 0
        assert report.failed == 0
        assert report.total_chars == 0
        assert report.failures == []

    def test_mixed_report(self, _target):
        report = ScrapeReport(
            results=[
                ScrapeResult(target=_target, success=True, char_count=100),
                ScrapeResult(target=_target, success=True, char_count=200),
                ScrapeResult(target=_target, success=False, error="Timeout"),
            ]
        )
        assert report.total == 3
        assert report.succeeded == 2
        assert report.failed == 1
        assert report.total_chars == 300
        assert len(report.failures) == 1

    def test_all_success(self, _target):
        report = ScrapeReport(
            results=[
                ScrapeResult(target=_target, success=True, char_count=500),
            ]
        )
        assert report.succeeded == 1
        assert report.failed == 0
        assert report.failures == []


class TestConfigConstants:
    """Tests for module-level configuration constants."""

    def test_base_url_is_https(self):
        assert BASE_URL.startswith("https://")

    def test_all_targets_nonempty(self):
        assert len(ALL_TARGETS) > 0

    def test_all_targets_is_union(self):
        expected = len(CORE_TARGETS) + len(DEPARTMENT_TARGETS) + len(RESOURCE_TARGETS)
        assert len(ALL_TARGETS) == expected

    def test_all_target_urls_are_kenyon(self):
        for target in ALL_TARGETS:
            assert target.url.startswith(BASE_URL), (
                f"{target.filename} URL doesn't start with {BASE_URL}"
            )

    def test_all_target_filenames_are_md(self):
        for target in ALL_TARGETS:
            assert target.filename.endswith(".md"), f"{target.filename} doesn't end with .md"

    def test_no_duplicate_filenames(self):
        filenames = [t.filename for t in ALL_TARGETS]
        assert len(filenames) == len(set(filenames)), "Duplicate filenames found"

    def test_no_duplicate_urls(self):
        urls = [t.url for t in ALL_TARGETS]
        assert len(urls) == len(set(urls)), "Duplicate URLs found"

    def test_valid_categories(self):
        valid_categories = {"departments", "courses", "faculty", "research", "advising"}
        for target in ALL_TARGETS:
            assert target.category in valid_categories, (
                f"{target.filename} has invalid category: {target.category}"
            )

    def test_reasonable_delay(self):
        assert REQUEST_DELAY_SECONDS >= 1.0, "Delay should be at least 1s to be respectful"

    def test_reasonable_concurrency(self):
        assert 1 <= MAX_CONCURRENT_SCRAPERS <= 5, "Concurrency should be 1-5 for a college site"

    def test_reasonable_retries(self):
        assert 1 <= MAX_RETRIES <= 5
