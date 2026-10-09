"""Unit tests for _extract_content helper in scraper module."""

from unittest.mock import MagicMock

from src.kenyon_bot.scraper import _extract_content


class TestExtractContent:
    """Tests for the content extraction logic."""

    def test_returns_markdown_from_simple_result(self):
        result = MagicMock()
        result.markdown = "# Hello World\n" * 10
        content = _extract_content(result)
        assert content == "# Hello World\n" * 10

    def test_returns_empty_for_none_markdown(self):
        result = MagicMock()
        result.markdown = None
        content = _extract_content(result)
        assert content == ""

    def test_returns_fit_markdown_when_available(self):
        result = MagicMock()
        result.markdown = "raw markdown content" * 10
        result.markdown_v2 = MagicMock()
        result.markdown_v2.fit_markdown = "clean fit markdown content" * 10
        content = _extract_content(result)
        assert content == "clean fit markdown content" * 10

    def test_falls_back_to_raw_when_fit_too_short(self):
        result = MagicMock()
        result.markdown = "raw markdown is longer" * 10
        result.markdown_v2 = MagicMock()
        result.markdown_v2.fit_markdown = "tiny"  # <50 chars
        content = _extract_content(result)
        assert content == "raw markdown is longer" * 10

    def test_falls_back_when_markdown_v2_is_none(self):
        result = MagicMock()
        result.markdown = "fallback content" * 10
        result.markdown_v2 = None
        content = _extract_content(result)
        assert content == "fallback content" * 10

    def test_handles_magic_mock_attributes(self):
        """MagicMock auto-creates attributes — should not crash."""
        result = MagicMock()
        # Don't set markdown explicitly — MagicMock returns another mock
        content = _extract_content(result)
        # Should return empty string since mock.markdown is not a str
        assert content == ""

    def test_handles_non_string_markdown(self):
        result = MagicMock()
        result.markdown = 12345  # not a string
        content = _extract_content(result)
        assert content == ""

    def test_handles_fit_markdown_not_string(self):
        result = MagicMock()
        result.markdown = "valid raw content here" * 10
        result.markdown_v2 = MagicMock()
        result.markdown_v2.fit_markdown = 42  # not a string
        content = _extract_content(result)
        assert content == "valid raw content here" * 10

    def test_prefers_fit_over_raw_when_both_good(self):
        result = MagicMock()
        result.markdown = "x" * 200
        result.markdown_v2 = MagicMock()
        result.markdown_v2.fit_markdown = "y" * 200
        content = _extract_content(result)
        assert content == "y" * 200

    def test_empty_string_markdown(self):
        result = MagicMock()
        result.markdown = ""
        content = _extract_content(result)
        assert content == ""
