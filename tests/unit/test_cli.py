"""Unit tests for CLI module."""

from unittest.mock import patch

import pytest

from src.kenyon_bot.cli import main, setup_logging


class TestSetupLogging:
    def test_default_level(self):
        import logging

        setup_logging(verbose=False)
        assert logging.getLogger().level == logging.INFO

    def test_verbose_level(self):
        import logging

        setup_logging(verbose=True)
        assert logging.getLogger().level == logging.DEBUG


class TestCLIMain:
    def test_creates_vault_directory(self, tmp_path):
        vault = tmp_path / "test-vault"
        with (
            patch("sys.argv", ["cli", "--vault", str(vault), "--targets", "core"]),
            patch("src.kenyon_bot.cli.scrape_targets"),
            patch("src.kenyon_bot.cli.asyncio") as mock_asyncio,
        ):
            from src.kenyon_bot.config import ScrapeReport

            mock_asyncio.run.return_value = ScrapeReport()
            with pytest.raises(SystemExit) as exc_info:
                main()
            # Exit code 0 because 0 failures (0 targets scraped)
            assert exc_info.value.code == 0
            assert vault.is_dir()

    def test_invalid_targets_arg(self):
        with (
            patch("sys.argv", ["cli", "--targets", "invalid"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()
        assert exc_info.value.code == 2  # argparse error

    def test_exit_code_1_on_failures(self, tmp_path):
        vault = tmp_path / "fail-vault"
        with (
            patch("sys.argv", ["cli", "--vault", str(vault), "--targets", "core"]),
            patch("src.kenyon_bot.cli.scrape_targets"),
            patch("src.kenyon_bot.cli.asyncio") as mock_asyncio,
        ):
            from src.kenyon_bot.config import ScrapeReport, ScrapeResult, ScrapeTarget

            target = ScrapeTarget(filename="t.md", url="https://x.com", category="departments")
            report = ScrapeReport(
                results=[ScrapeResult(target=target, success=False, error="fail")]
            )
            mock_asyncio.run.return_value = report
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
