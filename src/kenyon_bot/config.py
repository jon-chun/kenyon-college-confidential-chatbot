"""Configuration for Kenyon.edu scraping targets and vault structure."""

from dataclasses import dataclass, field
from pathlib import Path

# ── Vault layer directories ──────────────────────────────────────────────────

VAULT_ROOT = Path("Kenyon-Advisor-Wiki")
RAW_SOURCES_DIR = VAULT_ROOT / "00-Raw-Sources"
WIKI_DIR = VAULT_ROOT / "01-Wiki"
SCRATCH_DIR = VAULT_ROOT / "02-Scratch-Memory"

VAULT_DIRS = [RAW_SOURCES_DIR, WIKI_DIR, SCRATCH_DIR]

# ── Scraping configuration ───────────────────────────────────────────────────

BASE_URL = "https://www.kenyon.edu"

# Delay between requests (seconds) — be respectful to kenyon.edu
REQUEST_DELAY_SECONDS = 2.0

# Maximum concurrent scrapers
MAX_CONCURRENT_SCRAPERS = 3

# Request timeout (seconds)
REQUEST_TIMEOUT_SECONDS = 45

# Retry configuration
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2.0  # exponential backoff: 2^attempt seconds


@dataclass(frozen=True)
class ScrapeTarget:
    """A single page to scrape from kenyon.edu."""

    filename: str
    url: str
    category: str  # departments, courses, faculty, research, advising


# ── Stable Kenyon.edu targets (public, no login required) ────────────────────

CORE_TARGETS: list[ScrapeTarget] = [
    ScrapeTarget(
        filename="departments.md",
        url=f"{BASE_URL}/academics/departments-and-majors/",
        category="departments",
    ),
    ScrapeTarget(
        filename="catalog-main.md",
        url=f"{BASE_URL}/offices-and-services/registrar/kenyon-college-course-catalog/",
        category="courses",
    ),
    ScrapeTarget(
        filename="research-programs.md",
        url=f"{BASE_URL}/academics/student-research/",
        category="research",
    ),
    ScrapeTarget(
        filename="cascade-projects.md",
        url=f"{BASE_URL}/academics/student-research/cascade/cascade-project-descriptions/",
        category="research",
    ),
    ScrapeTarget(
        filename="advising-resources.md",
        url=f"{BASE_URL}/academics/advising-resources/",
        category="advising",
    ),
]

# Department-specific pages for deeper course/faculty info
DEPARTMENT_TARGETS: list[ScrapeTarget] = [
    ScrapeTarget(
        filename="biology.md",
        url=f"{BASE_URL}/academics/departments-and-majors/biology/",
        category="departments",
    ),
    ScrapeTarget(
        filename="chemistry.md",
        url=f"{BASE_URL}/academics/departments-and-majors/chemistry/",
        category="departments",
    ),
    ScrapeTarget(
        filename="english.md",
        url=f"{BASE_URL}/academics/departments-and-majors/english/",
        category="departments",
    ),
    ScrapeTarget(
        filename="mathematics.md",
        url=f"{BASE_URL}/academics/departments-and-majors/mathematics-and-statistics/",
        category="departments",
    ),
    ScrapeTarget(
        filename="neuroscience.md",
        url=f"{BASE_URL}/academics/departments-and-majors/neuroscience/",
        category="departments",
    ),
    ScrapeTarget(
        filename="physics.md",
        url=f"{BASE_URL}/academics/departments-and-majors/physics/",
        category="departments",
    ),
    ScrapeTarget(
        filename="political-science.md",
        url=f"{BASE_URL}/academics/departments-and-majors/political-science/",
        category="departments",
    ),
    ScrapeTarget(
        filename="psychology.md",
        url=f"{BASE_URL}/academics/departments-and-majors/psychology/",
        category="departments",
    ),
    ScrapeTarget(
        filename="economics.md",
        url=f"{BASE_URL}/academics/departments-and-majors/economics/",
        category="departments",
    ),
    ScrapeTarget(
        filename="history.md",
        url=f"{BASE_URL}/academics/departments-and-majors/history/",
        category="departments",
    ),
    ScrapeTarget(
        filename="sociology.md",
        url=f"{BASE_URL}/academics/departments-and-majors/sociology/",
        category="departments",
    ),
    ScrapeTarget(
        filename="philosophy.md",
        url=f"{BASE_URL}/academics/departments-and-majors/philosophy/",
        category="departments",
    ),
    ScrapeTarget(
        filename="art.md",
        url=f"{BASE_URL}/academics/departments-and-majors/studio-art/",
        category="departments",
    ),
    ScrapeTarget(
        filename="music.md",
        url=f"{BASE_URL}/academics/departments-and-majors/music/",
        category="departments",
    ),
    ScrapeTarget(
        filename="religious-studies.md",
        url=f"{BASE_URL}/academics/departments-and-majors/religious-studies/",
        category="departments",
    ),
    ScrapeTarget(
        filename="environmental-studies.md",
        url=f"{BASE_URL}/academics/departments-and-majors/environmental-studies/",
        category="departments",
    ),
    ScrapeTarget(
        filename="anthropology.md",
        url=f"{BASE_URL}/academics/departments-and-majors/anthropology/",
        category="departments",
    ),
    ScrapeTarget(
        filename="classics.md",
        url=f"{BASE_URL}/academics/departments-and-majors/classics/",
        category="departments",
    ),
    ScrapeTarget(
        filename="modern-languages-and-literatures.md",
        url=f"{BASE_URL}/academics/departments-and-majors/modern-languages-literatures/",
        category="departments",
    ),
    ScrapeTarget(
        filename="dance-drama-film.md",
        url=f"{BASE_URL}/academics/departments-and-majors/dance-drama-film/",
        category="departments",
    ),
]

# Academic centers, special programs, and additional resources
RESOURCE_TARGETS: list[ScrapeTarget] = [
    ScrapeTarget(
        filename="bfec.md",
        url=f"{BASE_URL}/academics/brown-family-environmental-center/",
        category="research",
    ),
    ScrapeTarget(
        filename="center-for-innovative-pedagogy.md",
        url=f"{BASE_URL}/offices-and-services/center-for-innovative-pedagogy/",
        category="advising",
    ),
    ScrapeTarget(
        filename="career-development.md",
        url=f"{BASE_URL}/offices-and-services/career-development-office/",
        category="advising",
    ),
    ScrapeTarget(
        filename="library.md",
        url=f"{BASE_URL}/offices-and-services/library/",
        category="research",
    ),
    ScrapeTarget(
        filename="off-campus-study.md",
        url=f"{BASE_URL}/academics/off-campus-study-opportunities/",
        category="advising",
    ),
    ScrapeTarget(
        filename="pre-professional.md",
        url=f"{BASE_URL}/academics/pre-professional-advising/",
        category="advising",
    ),
]

ALL_TARGETS: list[ScrapeTarget] = CORE_TARGETS + DEPARTMENT_TARGETS + RESOURCE_TARGETS


@dataclass
class ScrapeResult:
    """Result of scraping a single target."""

    target: ScrapeTarget
    success: bool
    markdown: str = ""
    error: str = ""
    char_count: int = 0
    attempts: int = 1


@dataclass
class ScrapeReport:
    """Summary report for a scraping session."""

    results: list[ScrapeResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def succeeded(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.success)

    @property
    def total_chars(self) -> int:
        return sum(r.char_count for r in self.results if r.success)

    @property
    def failures(self) -> list[ScrapeResult]:
        return [r for r in self.results if not r.success]
