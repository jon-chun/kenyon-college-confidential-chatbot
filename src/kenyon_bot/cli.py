"""CLI entry point for the Kenyon scraping pipeline."""

import asyncio
import logging
import sys
from pathlib import Path

from .config import ALL_TARGETS, CORE_TARGETS, DEPARTMENT_TARGETS, RESOURCE_TARGETS
from .scraper import scrape_targets
from .vault import create_vault, validate_vault


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    """Run the full scraping pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="Kenyon College Confidential Bot — Scraper")
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path("Kenyon-Advisor-Wiki"),
        help="Vault root directory (default: Kenyon-Advisor-Wiki)",
    )
    parser.add_argument(
        "--targets",
        choices=["all", "core", "departments", "resources"],
        default="all",
        help="Which target set to scrape",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=3,
        help="Max parallel scrapers (default: 3)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between requests per worker in seconds (default: 2.0)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Create vault structure
    vault_root = create_vault(args.vault)
    issues = validate_vault(vault_root)
    if issues:
        logger.error("Vault validation failed:")
        for issue in issues:
            logger.error("  - %s", issue)
        sys.exit(1)

    # Select targets
    target_map = {
        "all": ALL_TARGETS,
        "core": CORE_TARGETS,
        "departments": DEPARTMENT_TARGETS,
        "resources": RESOURCE_TARGETS,
    }
    targets = target_map[args.targets]
    logger.info("Scraping %d targets (%s) into %s", len(targets), args.targets, vault_root)

    # Run scraping
    report = asyncio.run(
        scrape_targets(
            targets=targets,
            max_concurrent=args.max_concurrent,
            delay=args.delay,
            vault_root=vault_root,
        )
    )

    # Report
    print(f"\n{'=' * 60}")
    print("Scraping Report")
    print(f"{'=' * 60}")
    print(f"Total targets:  {report.total}")
    print(f"Succeeded:      {report.succeeded}")
    print(f"Failed:         {report.failed}")
    print(f"Total chars:    {report.total_chars:,}")

    if report.failures:
        print("\nFailed targets:")
        for r in report.failures:
            print(f"  ✗ {r.target.filename}: {r.error}")

    print(f"\nFiles saved to: {vault_root / '00-Raw-Sources'}")

    sys.exit(1 if report.failed > 0 else 0)


if __name__ == "__main__":
    main()
