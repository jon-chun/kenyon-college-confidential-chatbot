"""Unit tests for vault module."""

from pathlib import Path

from src.kenyon_bot.vault import (
    CLAUDE_MD_TEMPLATE,
    INDEX_MD_TEMPLATE,
    create_vault,
    get_raw_source_files,
    save_scraped_content,
    validate_vault,
)


class TestCreateVault:
    """Tests for create_vault function."""

    def test_creates_all_directories(self, tmp_path: Path):
        vault = create_vault(tmp_path / "vault")
        assert (vault / "00-Raw-Sources").is_dir()
        assert (vault / "01-Wiki").is_dir()
        assert (vault / "02-Scratch-Memory").is_dir()

    def test_creates_claude_md(self, tmp_path: Path):
        vault = create_vault(tmp_path / "vault")
        claude_md = vault / "CLAUDE.md"
        assert claude_md.is_file()
        content = claude_md.read_text()
        assert "Kenyon Confidential Bot" in content
        assert "00-Raw-Sources" in content
        assert "01-Wiki" in content
        assert "02-Scratch-Memory" in content

    def test_creates_index_md(self, tmp_path: Path):
        vault = create_vault(tmp_path / "vault")
        index_md = vault / "index.md"
        assert index_md.is_file()
        assert "Index" in index_md.read_text()

    def test_idempotent(self, tmp_path: Path):
        vault_path = tmp_path / "vault"
        vault1 = create_vault(vault_path)
        vault2 = create_vault(vault_path)
        assert vault1 == vault2
        # Files should not be overwritten
        assert (vault2 / "CLAUDE.md").is_file()

    def test_does_not_overwrite_existing_claude_md(self, tmp_path: Path):
        vault_path = tmp_path / "vault"
        vault_path.mkdir()
        custom_content = "# Custom CLAUDE.md"
        (vault_path / "CLAUDE.md").write_text(custom_content)
        create_vault(vault_path)
        assert (vault_path / "CLAUDE.md").read_text() == custom_content

    def test_returns_vault_path(self, tmp_path: Path):
        vault = create_vault(tmp_path / "my-vault")
        assert vault == tmp_path / "my-vault"
        assert vault.exists()


class TestValidateVault:
    """Tests for validate_vault function."""

    def test_valid_vault(self, tmp_vault: Path):
        issues = validate_vault(tmp_vault)
        assert issues == []

    def test_missing_vault_root(self, tmp_path: Path):
        issues = validate_vault(tmp_path / "nonexistent")
        assert len(issues) == 1
        assert "does not exist" in issues[0]

    def test_missing_directory(self, tmp_vault: Path):
        import shutil

        shutil.rmtree(tmp_vault / "01-Wiki")
        issues = validate_vault(tmp_vault)
        assert any("01-Wiki" in issue for issue in issues)

    def test_missing_claude_md(self, tmp_vault: Path):
        (tmp_vault / "CLAUDE.md").unlink()
        issues = validate_vault(tmp_vault)
        assert any("CLAUDE.md" in issue for issue in issues)

    def test_missing_index_md(self, tmp_vault: Path):
        (tmp_vault / "index.md").unlink()
        issues = validate_vault(tmp_vault)
        assert any("index.md" in issue for issue in issues)

    def test_multiple_issues(self, tmp_path: Path):
        vault = tmp_path / "broken-vault"
        vault.mkdir()
        # Only create the root — everything else is missing
        issues = validate_vault(vault)
        assert len(issues) >= 4  # 3 dirs + CLAUDE.md + index.md


class TestSaveScrapedContent:
    """Tests for save_scraped_content function."""

    def test_saves_file(self, tmp_vault: Path):
        path = save_scraped_content("test.md", "# Test Content", root=tmp_vault)
        assert path.exists()
        assert path.read_text() == "# Test Content"

    def test_saves_to_raw_sources(self, tmp_vault: Path):
        path = save_scraped_content("biology.md", "# Biology", root=tmp_vault)
        assert path.parent.name == "00-Raw-Sources"

    def test_overwrites_existing(self, tmp_vault: Path):
        save_scraped_content("test.md", "v1", root=tmp_vault)
        save_scraped_content("test.md", "v2", root=tmp_vault)
        path = tmp_vault / "00-Raw-Sources" / "test.md"
        assert path.read_text() == "v2"

    def test_creates_directory_if_missing(self, tmp_path: Path):
        vault = tmp_path / "new-vault"
        path = save_scraped_content("test.md", "content", root=vault)
        assert path.exists()

    def test_utf8_content(self, tmp_vault: Path):
        content = "# Départment — Über Résumé"
        path = save_scraped_content("unicode.md", content, root=tmp_vault)
        assert path.read_text(encoding="utf-8") == content


class TestGetRawSourceFiles:
    """Tests for get_raw_source_files function."""

    def test_empty_vault(self, tmp_vault: Path):
        files = get_raw_source_files(tmp_vault)
        assert files == []

    def test_returns_md_files(self, tmp_vault: Path):
        raw_dir = tmp_vault / "00-Raw-Sources"
        (raw_dir / "biology.md").write_text("# Bio")
        (raw_dir / "chemistry.md").write_text("# Chem")
        files = get_raw_source_files(tmp_vault)
        assert len(files) == 2
        assert all(f.suffix == ".md" for f in files)

    def test_ignores_non_md_files(self, tmp_vault: Path):
        raw_dir = tmp_vault / "00-Raw-Sources"
        (raw_dir / "biology.md").write_text("# Bio")
        (raw_dir / "notes.txt").write_text("not markdown")
        (raw_dir / "data.json").write_text("{}")
        files = get_raw_source_files(tmp_vault)
        assert len(files) == 1

    def test_sorted_alphabetically(self, tmp_vault: Path):
        raw_dir = tmp_vault / "00-Raw-Sources"
        (raw_dir / "zebra.md").write_text("z")
        (raw_dir / "alpha.md").write_text("a")
        (raw_dir / "middle.md").write_text("m")
        files = get_raw_source_files(tmp_vault)
        names = [f.name for f in files]
        assert names == ["alpha.md", "middle.md", "zebra.md"]

    def test_nonexistent_vault(self, tmp_path: Path):
        files = get_raw_source_files(tmp_path / "nope")
        assert files == []


class TestTemplates:
    """Tests for CLAUDE.md and index.md templates."""

    def test_claude_md_has_required_sections(self):
        required = [
            "Identity",
            "Vault Structure",
            "Entity Types",
            "Page Template",
            "Cross-Linking Rules",
            "INGEST",
            "QUERY",
            "LINT",
        ]
        for section in required:
            assert section in CLAUDE_MD_TEMPLATE, f"Missing section: {section}"

    def test_claude_md_references_all_layers(self):
        assert "00-Raw-Sources" in CLAUDE_MD_TEMPLATE
        assert "01-Wiki" in CLAUDE_MD_TEMPLATE
        assert "02-Scratch-Memory" in CLAUDE_MD_TEMPLATE

    def test_index_md_is_placeholder(self):
        assert "auto-generated" in INDEX_MD_TEMPLATE.lower()
