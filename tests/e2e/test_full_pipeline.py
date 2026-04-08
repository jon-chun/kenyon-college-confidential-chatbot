"""End-to-end tests for the full scraping pipeline."""

import pytest

from src.kenyon_bot.config import ALL_TARGETS, CORE_TARGETS, DEPARTMENT_TARGETS
from src.kenyon_bot.scraper import scrape_targets
from src.kenyon_bot.vault import (
    create_vault,
    get_raw_source_files,
    validate_vault,
)


@pytest.mark.slow
@pytest.mark.e2e
class TestFullPipeline:
    """End-to-end: create vault → scrape all targets → validate results."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_full_core_pipeline(self, tmp_path):
        """Run complete pipeline with core targets."""
        # 1. Create vault
        vault = create_vault(tmp_path / "e2e-vault")
        assert validate_vault(vault) == []

        # 2. Scrape core targets
        report = await scrape_targets(
            targets=CORE_TARGETS,
            max_concurrent=2,
            delay=2.0,
            vault_root=vault,
        )

        # 3. Validate results
        assert report.total == len(CORE_TARGETS)
        assert report.succeeded >= 3, (
            f"Core pipeline: {report.succeeded}/{report.total} succeeded. "
            f"Failures: {[(r.target.filename, r.error) for r in report.failures]}"
        )

        # 4. Check files exist on disk
        files = get_raw_source_files(vault)
        assert len(files) >= 3

        # 5. Check total content is substantial
        assert report.total_chars > 5000, (
            f"Total scraped content too small: {report.total_chars} chars"
        )

        # 6. Vault should still be valid
        assert validate_vault(vault) == []

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_departments_pipeline(self, tmp_path):
        """Scrape department-specific pages."""
        vault = create_vault(tmp_path / "dept-vault")

        # Scrape first 5 departments for speed
        targets = DEPARTMENT_TARGETS[:5]
        report = await scrape_targets(
            targets=targets,
            max_concurrent=2,
            delay=2.0,
            vault_root=vault,
        )

        assert report.succeeded >= 3, f"Departments: {report.succeeded}/{report.total} succeeded"

        # Check that files contain department-relevant content
        files = get_raw_source_files(vault)
        for f in files:
            content = f.read_text()
            assert len(content) > 200, f"{f.name} too short"

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_full_all_targets_pipeline(self, tmp_path):
        """Scrape ALL targets — the full dataset. Longest test."""
        vault = create_vault(tmp_path / "full-vault")

        report = await scrape_targets(
            targets=ALL_TARGETS,
            max_concurrent=3,
            delay=2.0,
            vault_root=vault,
        )

        # With 30+ targets, expect at least 80% success
        min_success = int(len(ALL_TARGETS) * 0.8)
        assert report.succeeded >= min_success, (
            f"Full pipeline: {report.succeeded}/{report.total} succeeded "
            f"(need {min_success}). Failures: "
            f"{[(r.target.filename, r.error) for r in report.failures]}"
        )

        # Check total content
        assert report.total_chars > 50000, f"Full scrape too small: {report.total_chars:,} chars"

        files = get_raw_source_files(vault)
        assert len(files) >= min_success


@pytest.mark.slow
@pytest.mark.e2e
class TestPipelineEdgeCases:
    """Edge case tests for the pipeline."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(120)
    async def test_rescrape_overwrites(self, tmp_path):
        """Verify that re-scraping updates existing files."""
        vault = create_vault(tmp_path / "rescrape-vault")
        targets = CORE_TARGETS[:1]

        # First scrape
        report1 = await scrape_targets(
            targets=targets,
            max_concurrent=1,
            delay=2.0,
            vault_root=vault,
        )

        if report1.succeeded == 0:
            pytest.skip("First scrape failed — network issue")

        files1 = get_raw_source_files(vault)
        first_content_len = len(files1[0].read_text())
        assert first_content_len > 100

        # Second scrape (should overwrite)
        await scrape_targets(
            targets=targets,
            max_concurrent=1,
            delay=2.0,
            vault_root=vault,
        )

        files2 = get_raw_source_files(vault)
        assert len(files2) == len(files1), "File count changed after rescrape"
        content2 = files2[0].read_text()
        assert len(content2) > 100, "Rescrape produced empty file"

    @pytest.mark.asyncio
    @pytest.mark.timeout(120)
    async def test_concurrent_workers_produce_correct_count(self, tmp_path):
        """Verify concurrent workers don't lose or duplicate results."""
        vault = create_vault(tmp_path / "concurrent-vault")
        targets = CORE_TARGETS[:4]

        report = await scrape_targets(
            targets=targets,
            max_concurrent=3,
            delay=1.0,
            vault_root=vault,
        )

        # Total results should equal target count regardless of concurrency
        assert report.total == len(targets)
        # No file should be duplicated
        files = get_raw_source_files(vault)
        filenames = [f.name for f in files]
        assert len(filenames) == len(set(filenames)), "Duplicate files found"
