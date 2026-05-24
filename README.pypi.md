# pbi-cli-codex

Codex-focused adaptation of Mina Saad's original
[`MinaSaad1/pbi-cli`](https://github.com/MinaSaad1/pbi-cli).

The original project provides the Power BI CLI, Power BI Desktop interop, PBIR
commands, and the first bundled Power BI skills. This fork keeps that foundation
and adds Codex installation support:

- `pbi-cli skills install --agent codex`
- Codex skill installation into `~/.agents/skills`
- Codex global guidance in `~/.codex/AGENTS.md`
- Windows and macOS installer scripts

## Install

Windows:

```powershell
git clone https://github.com/Juanxchito/pbi-cli-codex.git
cd pbi-cli-codex
powershell -ExecutionPolicy Bypass -File .\scripts\codex\install-codex-windows.ps1
pbi connect
```

macOS:

```bash
git clone https://github.com/Juanxchito/pbi-cli-codex.git
cd pbi-cli-codex
bash scripts/codex/install-codex-macos.sh
```

Windows is recommended for semantic model work because Power BI Desktop runs on
Windows. macOS can still use the Codex skills and PBIR/report-file commands.

## Verify

```bash
pbi-cli skills list --agent codex
pbi --json setup --info
```

## Attribution

This repository is derived from `MinaSaad1/pbi-cli`. Credit for the core CLI,
Power BI Desktop interop, PBIR commands, and original skills belongs to Mina
Saad and the pbi-cli contributors. This fork exists to make that work easier to
install and use from Codex.
