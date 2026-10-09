"""Tests that validate the quality and integrity of actual scraped data in the vault."""

from pathlib import Path

import pytest

VAULT_ROOT = Path("Kenyon-Advisor-Wiki")
RAW_DIR = VAULT_ROOT / "00-Raw-Sources"


def _scraped_files() -> list[Path]:
    if not RAW_DIR.exists():
        pytest.skip("Vault not populated — run scraper first")
    files = sorted(RAW_DIR.glob("*.md"))
    if not files:
        pytest.skip("No scraped files found")
    return files


@pytest.mark.integration
class TestScrapedFileInventory:
    """Verify all expected files exist and are non-empty."""

    EXPECTED_CORE = [
        "departments.md",
        "catalog-main.md",
        "research-programs.md",
        "cascade-projects.md",
        "advising-resources.md",
    ]

    EXPECTED_DEPARTMENTS = [
        "biology.md",
        "chemistry.md",
        "english.md",
        "neuroscience.md",
        "physics.md",
        "political-science.md",
        "psychology.md",
        "economics.md",
        "history.md",
        "sociology.md",
        "philosophy.md",
        "music.md",
        "religious-studies.md",
        "environmental-studies.md",
        "anthropology.md",
        "classics.md",
        "modern-languages-and-literatures.md",
        "dance-drama-film.md",
        "mathematics.md",
        "art.md",
    ]

    EXPECTED_RESOURCES = [
        "bfec.md",
        "center-for-innovative-pedagogy.md",
        "career-development.md",
        "library.md",
        "off-campus-study.md",
        "pre-professional.md",
    ]

    def test_all_core_files_exist(self):
        _scraped_files()
        for name in self.EXPECTED_CORE:
            path = RAW_DIR / name
            assert path.exists(), f"Missing core file: {name}"
            assert path.stat().st_size > 0, f"Empty core file: {name}"

    def test_all_department_files_exist(self):
        _scraped_files()
        for name in self.EXPECTED_DEPARTMENTS:
            path = RAW_DIR / name
            assert path.exists(), f"Missing department file: {name}"
            assert path.stat().st_size > 0, f"Empty department file: {name}"

    def test_all_resource_files_exist(self):
        _scraped_files()
        for name in self.EXPECTED_RESOURCES:
            path = RAW_DIR / name
            assert path.exists(), f"Missing resource file: {name}"
            assert path.stat().st_size > 0, f"Empty resource file: {name}"

    def test_total_file_count(self):
        files = _scraped_files()
        expected = (
            len(self.EXPECTED_CORE) + len(self.EXPECTED_DEPARTMENTS) + len(self.EXPECTED_RESOURCES)
        )
        assert len(files) == expected, (
            f"Expected {expected} files, found {len(files)}: {[f.name for f in files]}"
        )

    def test_no_unexpected_files(self):
        files = _scraped_files()
        expected_names = set(
            self.EXPECTED_CORE + self.EXPECTED_DEPARTMENTS + self.EXPECTED_RESOURCES
        )
        actual_names = {f.name for f in files}
        unexpected = actual_names - expected_names
        assert not unexpected, f"Unexpected files: {unexpected}"


@pytest.mark.integration
class TestScrapedContentQuality:
    """Validate the actual content quality of scraped files."""

    def test_no_file_is_pure_html(self):
        """Scraped content should be Markdown, not raw HTML."""
        for f in _scraped_files():
            content = f.read_text(encoding="utf-8")
            # Should not contain HTML document structure
            assert "<html" not in content.lower(), f"{f.name} contains <html>"
            assert "<body" not in content.lower(), f"{f.name} contains <body>"
            assert "<!DOCTYPE" not in content, f"{f.name} contains <!DOCTYPE>"

    def test_no_file_is_too_short(self):
        """Every file should have meaningful content (>500 chars)."""
        for f in _scraped_files():
            content = f.read_text(encoding="utf-8")
            assert len(content) > 500, (
                f"{f.name} is only {len(content)} chars — likely a failed scrape"
            )

    def test_no_file_is_only_boilerplate(self):
        """Files should have more than just nav/footer boilerplate."""
        for f in _scraped_files():
            content = f.read_text(encoding="utf-8")
            # Strip common boilerplate patterns
            stripped = content
            for pattern in ["Site Menu", "Search", "Submit", "Close", "Skip to main"]:
                stripped = stripped.replace(pattern, "")
            # After stripping, should still have substantial content
            assert len(stripped.strip()) > 200, f"{f.name} appears to be mostly boilerplate"

    def test_files_are_valid_utf8(self):
        """All files should be valid UTF-8."""
        for f in _scraped_files():
            try:
                f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pytest.fail(f"{f.name} is not valid UTF-8")

    def test_no_null_bytes(self):
        """Files should not contain null bytes (sign of binary content)."""
        for f in _scraped_files():
            content = f.read_bytes()
            assert b"\x00" not in content, f"{f.name} contains null bytes"


@pytest.mark.integration
class TestDepartmentsPageContent:
    """Validate the main departments listing has expected content."""

    @pytest.fixture
    def departments_content(self) -> str:
        path = RAW_DIR / "departments.md"
        if not path.exists():
            pytest.skip("departments.md not found")
        return path.read_text(encoding="utf-8")

    def test_contains_biology(self, departments_content):
        assert "biology" in departments_content.lower()

    def test_contains_english(self, departments_content):
        assert "english" in departments_content.lower()

    def test_contains_multiple_departments(self, departments_content):
        dept_keywords = [
            "biology",
            "chemistry",
            "economics",
            "english",
            "history",
            "mathematics",
            "physics",
            "psychology",
        ]
        found = sum(1 for k in dept_keywords if k in departments_content.lower())
        assert found >= 6, f"Only found {found}/8 expected departments in listing"

    def test_contains_links(self, departments_content):
        """Department listing should contain links to department pages."""
        link_count = departments_content.count("](")
        assert link_count >= 10, f"Only {link_count} links found — expected many department links"


@pytest.mark.integration
class TestCatalogContent:
    """Validate the course catalog has expected content."""

    @pytest.fixture
    def catalog_content(self) -> str:
        path = RAW_DIR / "catalog-main.md"
        if not path.exists():
            pytest.skip("catalog-main.md not found")
        return path.read_text(encoding="utf-8")

    def test_catalog_is_substantial(self, catalog_content):
        assert len(catalog_content) > 5000, "Catalog seems too short"

    def test_catalog_mentions_courses(self, catalog_content):
        course_terms = ["course", "credit", "prerequisite", "semester", "requirement"]
        found = sum(1 for t in course_terms if t in catalog_content.lower())
        assert found >= 2, "Catalog doesn't mention enough course-related terms"


@pytest.mark.integration
class TestResearchContent:
    """Validate research pages have expected content."""

    @pytest.fixture
    def research_content(self) -> str:
        path = RAW_DIR / "research-programs.md"
        if not path.exists():
            pytest.skip("research-programs.md not found")
        return path.read_text(encoding="utf-8")

    def test_mentions_research(self, research_content):
        assert "research" in research_content.lower()

    def test_mentions_students_or_faculty(self, research_content):
        content_lower = research_content.lower()
        assert "student" in content_lower or "faculty" in content_lower


@pytest.mark.integration
class TestDepartmentPageContent:
    """Validate individual department pages have expected structure."""

    SAMPLE_DEPARTMENTS = ["biology.md", "english.md", "chemistry.md", "physics.md"]

    def test_department_pages_have_kenyon_content(self):
        """Each department page should reference Kenyon or the department name."""
        _scraped_files()
        for name in self.SAMPLE_DEPARTMENTS:
            path = RAW_DIR / name
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8").lower()
            dept_name = name.replace(".md", "").replace("-", " ")
            assert "kenyon" in content or dept_name in content, (
                f"{name} doesn't mention Kenyon or {dept_name}"
            )

    def test_department_pages_have_links(self):
        """Department pages should contain internal links."""
        _scraped_files()
        for name in self.SAMPLE_DEPARTMENTS:
            path = RAW_DIR / name
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            link_count = content.count("](")
            assert link_count >= 3, (
                f"{name} has only {link_count} links — expected department navigation"
            )


@pytest.mark.integration
class TestVaultIntegrity:
    """Validate vault structure alongside scraped data."""

    def test_vault_directories_exist(self):
        assert VAULT_ROOT.is_dir(), "Vault root missing"
        assert (VAULT_ROOT / "00-Raw-Sources").is_dir()
        assert (VAULT_ROOT / "01-Wiki").is_dir()
        assert (VAULT_ROOT / "02-Scratch-Memory").is_dir()

    def test_claude_md_exists(self):
        claude_md = VAULT_ROOT / "CLAUDE.md"
        assert claude_md.is_file(), "CLAUDE.md missing"
        content = claude_md.read_text()
        assert "Kenyon Confidential Bot" in content

    def test_index_md_exists(self):
        assert (VAULT_ROOT / "index.md").is_file()

    def test_raw_sources_not_in_wiki(self):
        """Raw source files should only be in 00-Raw-Sources, not 01-Wiki."""
        wiki_dir = VAULT_ROOT / "01-Wiki"
        if wiki_dir.exists():
            wiki_files = list(wiki_dir.glob("*.md"))
            raw_names = {f.name for f in (VAULT_ROOT / "00-Raw-Sources").glob("*.md")}
            wiki_names = {f.name for f in wiki_files}
            overlap = raw_names & wiki_names
            assert not overlap, f"Files appear in both 00-Raw-Sources and 01-Wiki: {overlap}"

    def test_total_scraped_size_reasonable(self):
        """Total scraped data should be between 50KB and 10MB."""
        total = sum(f.stat().st_size for f in (VAULT_ROOT / "00-Raw-Sources").glob("*.md"))
        assert total > 50_000, f"Total scraped data too small: {total:,} bytes"
        assert total < 10_000_000, f"Total scraped data suspiciously large: {total:,} bytes"
