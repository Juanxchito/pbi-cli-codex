"""AGENTS.md snippet management for Codex integration."""

from __future__ import annotations

import os
from pathlib import Path

import click


def _codex_home() -> Path:
    """Return the Codex home directory."""
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


CODEX_AGENTS_MD_PATH = _codex_home() / "AGENTS.md"

_PBI_CLI_MARKER_START = "<!-- pbi-cli-codex:start -->"
_PBI_CLI_MARKER_END = "<!-- pbi-cli-codex:end -->"

_PBI_CLI_CODEX_AGENTS_SNIPPET = (
    "\n"
    "<!-- pbi-cli-codex:start -->\n"
    "# Power BI CLI (pbi-cli)\n"
    "\n"
    "When working with Power BI, DAX, semantic models, PBIR reports, "
    "or data modeling, invoke the relevant pbi-cli skill before responding:\n"
    "\n"
    "**Semantic Model (requires `pbi connect`):**\n"
    "- **power-bi-dax** -- DAX queries, measures, calculations\n"
    "- **power-bi-modeling** -- tables, columns, measures, relationships\n"
    "- **power-bi-deployment** -- TMDL export/import, transactions, diff\n"
    "- **power-bi-docs** -- model documentation, data dictionary\n"
    "- **power-bi-partitions** -- partitions, M expressions, data sources\n"
    "- **power-bi-security** -- RLS roles, perspectives, access control\n"
    "- **power-bi-diagnostics** -- troubleshooting, tracing, setup\n"
    "\n"
    "**Report Layer (no connection needed):**\n"
    "- **power-bi-report** -- scaffold, validate, preview PBIR reports\n"
    "- **power-bi-visuals** -- add, bind, update, bulk-manage visuals\n"
    "- **power-bi-pages** -- pages, bookmarks, visibility, drillthrough\n"
    "- **power-bi-themes** -- themes, conditional formatting, styling\n"
    "- **power-bi-filters** -- page and visual filters (TopN, date, categorical)\n"
    "- **power-bi-custom-visuals** -- build .pbiviz custom visuals "
    "(TS scaffold, tsc loop, package, import)\n"
    "\n"
    "Critical: Multi-line DAX (VAR/RETURN) cannot be passed via `-e`. "
    "Use `--file` or stdin piping instead. See power-bi-dax skill.\n"
    "<!-- pbi-cli-codex:end -->\n"
)


def ensure_codex_agents_snippet() -> None:
    """Append pbi-cli section to ~/.codex/AGENTS.md if not already present."""
    if CODEX_AGENTS_MD_PATH.exists():
        existing = CODEX_AGENTS_MD_PATH.read_text(encoding="utf-8")
        if _PBI_CLI_MARKER_START in existing:
            return
    else:
        CODEX_AGENTS_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
        existing = ""

    new_content = existing.rstrip() + _PBI_CLI_CODEX_AGENTS_SNIPPET
    CODEX_AGENTS_MD_PATH.write_text(new_content, encoding="utf-8")
    click.echo("  Added pbi-cli section to ~/.codex/AGENTS.md", err=True)


def remove_codex_agents_snippet() -> None:
    """Remove pbi-cli section from ~/.codex/AGENTS.md if present."""
    if not CODEX_AGENTS_MD_PATH.exists():
        return

    content = CODEX_AGENTS_MD_PATH.read_text(encoding="utf-8")
    if _PBI_CLI_MARKER_START not in content:
        return

    start_idx = content.index(_PBI_CLI_MARKER_START)
    end_idx = content.index(_PBI_CLI_MARKER_END) + len(_PBI_CLI_MARKER_END)

    before = content[:start_idx].rstrip()
    after = content[end_idx:].lstrip("\n")

    cleaned = before
    if after:
        cleaned = before + "\n\n" + after
    cleaned = cleaned.rstrip() + "\n" if cleaned.strip() else ""

    CODEX_AGENTS_MD_PATH.write_text(cleaned, encoding="utf-8")
    click.echo("  Removed pbi-cli section from ~/.codex/AGENTS.md", err=True)
