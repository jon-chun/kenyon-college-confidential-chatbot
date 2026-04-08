"""Shared test fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def tmp_vault(tmp_path: Path) -> Path:
    """Create a temporary vault directory structure for testing."""
    from src.kenyon_bot.vault import create_vault

    vault = create_vault(tmp_path / "test-vault")
    return vault


@pytest.fixture
def sample_markdown() -> str:
    """Sample Markdown content mimicking a scraped Kenyon page."""
    return """\
# Biology Department

Kenyon's Biology Department offers a rigorous curriculum spanning molecular
biology, ecology, evolution, and neuroscience.

## Faculty

- **Dr. Jane Smith** — Molecular Biology, Cell Signaling
- **Dr. John Doe** — Ecology, Conservation Biology
- **Dr. Alice Johnson** — Neuroscience, Behavioral Biology

## Courses

### BIOL 101 — Introductory Biology
An introduction to the fundamental principles of biology.
Prerequisites: None.

### BIOL 201 — Cell Biology
Study of cell structure and function at the molecular level.
Prerequisites: BIOL 101, CHEM 121.

### BIOL 301 — Ecology
Principles of ecology including population dynamics and ecosystems.
Prerequisites: BIOL 101.

## Research Opportunities

Students can participate in Summer Scholars research with faculty mentors.
The Brown Family Environmental Center (BFEC) offers field research opportunities.

## Related

- [Chemistry Department](/academics/departments-and-majors/chemistry/)
- [Neuroscience Program](/academics/departments-and-majors/neuroscience/)
- [Environmental Studies](/academics/departments-and-majors/environmental-studies/)
"""


@pytest.fixture
def sample_targets():
    """A small set of test targets."""
    from src.kenyon_bot.config import ScrapeTarget

    return [
        ScrapeTarget(
            filename="test-departments.md",
            url="https://www.kenyon.edu/academics/departments-and-majors/",
            category="departments",
        ),
        ScrapeTarget(
            filename="test-research.md",
            url="https://www.kenyon.edu/academics/student-research/",
            category="research",
        ),
    ]
