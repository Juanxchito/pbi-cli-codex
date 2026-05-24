"""Tests for Codex AGENTS.md snippet injection and removal."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_codex_agents_md(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect CODEX_AGENTS_MD_PATH to a temp directory."""
    agents_md = tmp_path / ".codex" / "AGENTS.md"
    monkeypatch.setattr("pbi_cli.core.codex_integration.CODEX_AGENTS_MD_PATH", agents_md)
    return agents_md


def _get_funcs():
    """Lazy import to avoid import side effects at collection time."""
    from pbi_cli.core.codex_integration import (
        _PBI_CLI_MARKER_END,
        _PBI_CLI_MARKER_START,
        ensure_codex_agents_snippet,
        remove_codex_agents_snippet,
    )

    return (
        ensure_codex_agents_snippet,
        remove_codex_agents_snippet,
        _PBI_CLI_MARKER_START,
        _PBI_CLI_MARKER_END,
    )


class TestEnsureCodexAgentsSnippet:
    def test_creates_file_when_missing(self, tmp_codex_agents_md: Path) -> None:
        ensure, _, start, end = _get_funcs()
        assert not tmp_codex_agents_md.exists()
        ensure()
        assert tmp_codex_agents_md.exists()
        content = tmp_codex_agents_md.read_text(encoding="utf-8")
        assert start in content
        assert end in content
        assert "power-bi-dax" in content

    def test_appends_to_existing(self, tmp_codex_agents_md: Path) -> None:
        ensure, _, start, end = _get_funcs()
        tmp_codex_agents_md.parent.mkdir(parents=True, exist_ok=True)
        tmp_codex_agents_md.write_text("# My Preferences\n\n- Ask first\n", encoding="utf-8")
        ensure()
        content = tmp_codex_agents_md.read_text(encoding="utf-8")
        assert content.startswith("# My Preferences")
        assert "- Ask first" in content
        assert start in content
        assert end in content

    def test_is_idempotent(self, tmp_codex_agents_md: Path) -> None:
        ensure, _, _, _ = _get_funcs()
        tmp_codex_agents_md.parent.mkdir(parents=True, exist_ok=True)
        tmp_codex_agents_md.write_text("# Existing\n", encoding="utf-8")
        ensure()
        first_content = tmp_codex_agents_md.read_text(encoding="utf-8")
        ensure()
        second_content = tmp_codex_agents_md.read_text(encoding="utf-8")
        assert first_content == second_content


class TestRemoveCodexAgentsSnippet:
    def test_removes_snippet(self, tmp_codex_agents_md: Path) -> None:
        ensure, remove, start, end = _get_funcs()
        tmp_codex_agents_md.parent.mkdir(parents=True, exist_ok=True)
        tmp_codex_agents_md.write_text("# Existing\n", encoding="utf-8")
        ensure()
        assert start in tmp_codex_agents_md.read_text(encoding="utf-8")
        remove()
        content = tmp_codex_agents_md.read_text(encoding="utf-8")
        assert start not in content
        assert end not in content

    def test_preserves_other_content(self, tmp_codex_agents_md: Path) -> None:
        ensure, remove, start, _ = _get_funcs()
        tmp_codex_agents_md.parent.mkdir(parents=True, exist_ok=True)
        tmp_codex_agents_md.write_text("# My Preferences\n\n- Ask first\n", encoding="utf-8")
        ensure()
        remove()
        content = tmp_codex_agents_md.read_text(encoding="utf-8")
        assert "# My Preferences" in content
        assert "- Ask first" in content
        assert start not in content

    def test_noop_when_not_present(self, tmp_codex_agents_md: Path) -> None:
        _, remove, _, _ = _get_funcs()
        tmp_codex_agents_md.parent.mkdir(parents=True, exist_ok=True)
        original = "# My Preferences\n\n- Ask first\n"
        tmp_codex_agents_md.write_text(original, encoding="utf-8")
        remove()
        assert tmp_codex_agents_md.read_text(encoding="utf-8") == original

    def test_noop_when_file_missing(self, tmp_codex_agents_md: Path) -> None:
        _, remove, _, _ = _get_funcs()
        assert not tmp_codex_agents_md.exists()
        remove()
        assert not tmp_codex_agents_md.exists()
