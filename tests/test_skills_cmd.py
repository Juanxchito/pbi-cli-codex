"""Tests for multi-agent skill installation."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from pbi_cli.main_pbi_cli import cli


def test_codex_install_copies_skill_resources(
    cli_runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Codex install should copy bundled files adjacent to SKILL.md."""
    target_dir = tmp_path / "skills"
    agents_md = tmp_path / ".codex" / "AGENTS.md"
    monkeypatch.setattr("pbi_cli.core.codex_integration.CODEX_AGENTS_MD_PATH", agents_md)

    result = cli_runner.invoke(
        cli,
        [
            "skills",
            "install",
            "--agent",
            "codex",
            "--target-dir",
            str(target_dir),
            "--skill",
            "power-bi-custom-visuals",
            "--yes",
        ],
    )

    assert result.exit_code == 0
    skill_dir = target_dir / "power-bi-custom-visuals"
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "AGENTS-template.md").exists()
    assert "<!-- pbi-cli-codex:start -->" in agents_md.read_text(encoding="utf-8")


def test_codex_uninstall_removes_global_snippet(
    cli_runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Uninstalling all Codex skills removes the global routing block."""
    target_dir = tmp_path / "skills"
    agents_md = tmp_path / ".codex" / "AGENTS.md"
    monkeypatch.setattr("pbi_cli.core.codex_integration.CODEX_AGENTS_MD_PATH", agents_md)

    install_result = cli_runner.invoke(
        cli,
        [
            "skills",
            "install",
            "--agent",
            "codex",
            "--target-dir",
            str(target_dir),
            "--skill",
            "power-bi-dax",
            "--yes",
        ],
    )
    assert install_result.exit_code == 0

    uninstall_result = cli_runner.invoke(
        cli,
        [
            "skills",
            "uninstall",
            "--agent",
            "codex",
            "--target-dir",
            str(target_dir),
        ],
    )

    assert uninstall_result.exit_code == 0
    assert "<!-- pbi-cli-codex:start -->" not in agents_md.read_text(encoding="utf-8")
