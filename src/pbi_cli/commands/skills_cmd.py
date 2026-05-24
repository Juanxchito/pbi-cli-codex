"""Skill installer commands for agent integrations."""

from __future__ import annotations

import importlib.resources
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.abc import Traversable

import click

CLAUDE_SKILLS_TARGET_DIR = Path.home() / ".claude" / "skills"
CODEX_SKILLS_TARGET_DIR = Path.home() / ".agents" / "skills"

AGENT_LABELS = {
    "claude": "Claude Code",
    "codex": "Codex",
}

AGENT_SKILL_TARGETS = {
    "claude": CLAUDE_SKILLS_TARGET_DIR,
    "codex": CODEX_SKILLS_TARGET_DIR,
}


def _get_bundled_skills() -> dict[str, Traversable]:
    """Return a mapping of skill-name -> Traversable for each bundled skill."""
    skills_pkg = importlib.resources.files("pbi_cli.skills")
    result: dict[str, Traversable] = {}
    for item in skills_pkg.iterdir():
        if item.is_dir() and (item / "SKILL.md").is_file():
            result[item.name] = item
    return result


def _get_target_dir(agent: str, target_dir: Path | None = None) -> Path:
    """Return the directory where skills should be installed for an agent."""
    if target_dir is not None:
        return target_dir.expanduser()
    return AGENT_SKILL_TARGETS[agent]


def _is_installed(
    skill_name: str,
    agent: str = "claude",
    target_dir: Path | None = None,
) -> bool:
    """Check if a skill is already installed for the selected agent."""
    return (_get_target_dir(agent, target_dir) / skill_name / "SKILL.md").exists()


def _copy_traversable(source: Traversable, target: Path) -> None:
    """Copy an importlib resource tree to a filesystem path."""
    if source.is_dir():
        target.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            if child.name == "__pycache__":
                continue
            _copy_traversable(child, target / child.name)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())


@click.group("skills")
def skills() -> None:
    """Manage agent skills for Power BI workflows."""


@skills.command("list")
@click.option(
    "--agent",
    type=click.Choice(["claude", "codex"], case_sensitive=False),
    default="claude",
    show_default=True,
    help="Agent integration to inspect.",
)
@click.option(
    "--target-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Override the skills directory.",
)
def skills_list(agent: str, target_dir: Path | None) -> None:
    """List available and installed skills."""
    agent = agent.lower()
    bundled = _get_bundled_skills()
    resolved_target_dir = _get_target_dir(agent, target_dir)
    if not bundled:
        click.echo("No bundled skills found.", err=True)
        return

    click.echo(f"Available Power BI skills for {AGENT_LABELS[agent]}:\n", err=True)
    for name in sorted(bundled):
        status = "installed" if _is_installed(name, agent, target_dir) else "not installed"
        click.echo(f"  {name:<30} [{status}]", err=True)
    click.echo(
        f"\nTarget directory: {resolved_target_dir}",
        err=True,
    )


@skills.command("install")
@click.option("--skill", "skill_name", default=None, help="Install a specific skill.")
@click.option("--force", is_flag=True, default=False, help="Overwrite existing installations.")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt.")
@click.option(
    "--agent",
    type=click.Choice(["claude", "codex"], case_sensitive=False),
    default="claude",
    show_default=True,
    help="Agent integration to install for.",
)
@click.option(
    "--target-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Override the skills directory.",
)
def skills_install(
    skill_name: str | None,
    force: bool,
    yes: bool,
    agent: str,
    target_dir: Path | None,
) -> None:
    """Install Power BI skills and register agent guidance."""
    agent = agent.lower()
    bundled = _get_bundled_skills()
    resolved_target_dir = _get_target_dir(agent, target_dir)
    if not bundled:
        click.echo("No bundled skills found.", err=True)
        return

    if skill_name and skill_name not in bundled:
        raise click.ClickException(
            f"Unknown skill '{skill_name}'. Available: {', '.join(sorted(bundled))}"
        )

    to_install = (
        {skill_name: bundled[skill_name]} if skill_name and skill_name in bundled else bundled
    )

    if not yes:
        click.echo(f"This command will modify your global {AGENT_LABELS[agent]} configuration:\n")
        skills_glob = str(resolved_target_dir / "power-bi-*")
        click.echo(f"  {skills_glob:<52} copy {len(to_install)} skill folder(s)")
        if agent == "claude":
            click.echo(f"  {'~/.claude/CLAUDE.md':<52} append pbi-cli skill trigger block")
        else:
            click.echo(f"  {'~/.codex/AGENTS.md':<52} append pbi-cli skill trigger block")
        click.echo(f"\nThis affects ALL {AGENT_LABELS[agent]} sessions, not just Power BI work.")
        if not click.confirm("\nProceed?", default=False):
            click.echo("Aborted.")
            return

    installed_count = 0
    for name, source in sorted(to_install.items()):
        skill_target_dir = resolved_target_dir / name
        if skill_target_dir.exists() and not force:
            click.echo(f"  {name}: already installed (use --force to overwrite)", err=True)
            continue

        if skill_target_dir.exists():
            shutil.rmtree(skill_target_dir)
        _copy_traversable(source, skill_target_dir)
        installed_count += 1
        click.echo(f"  {name}: installed", err=True)

    if installed_count > 0:
        if agent == "claude":
            from pbi_cli.core.claude_integration import ensure_claude_md_snippet

            ensure_claude_md_snippet()
        else:
            from pbi_cli.core.codex_integration import ensure_codex_agents_snippet

            ensure_codex_agents_snippet()

    click.echo(f"\n{installed_count} skill(s) installed to {resolved_target_dir}", err=True)


@skills.command("uninstall")
@click.option("--skill", "skill_name", default=None, help="Uninstall a specific skill.")
@click.option(
    "--agent",
    type=click.Choice(["claude", "codex"], case_sensitive=False),
    default="claude",
    show_default=True,
    help="Agent integration to uninstall from.",
)
@click.option(
    "--target-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Override the skills directory.",
)
def skills_uninstall(skill_name: str | None, agent: str, target_dir: Path | None) -> None:
    """Remove installed skills for the selected agent."""
    agent = agent.lower()
    bundled = _get_bundled_skills()
    resolved_target_dir = _get_target_dir(agent, target_dir)
    names = [skill_name] if skill_name else sorted(bundled)

    removed_count = 0
    for name in names:
        skill_target_dir = resolved_target_dir / name
        if not skill_target_dir.exists():
            click.echo(f"  {name}: not installed", err=True)
            continue

        shutil.rmtree(skill_target_dir)
        removed_count += 1
        click.echo(f"  {name}: removed", err=True)

    click.echo(f"\n{removed_count} skill(s) removed.", err=True)

    if skill_name is None:
        if agent == "claude":
            from pbi_cli.core.claude_integration import remove_claude_md_snippet

            remove_claude_md_snippet()
        else:
            from pbi_cli.core.codex_integration import remove_codex_agents_snippet

            remove_codex_agents_snippet()
