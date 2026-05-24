# pbi-cli for Codex

This fork adds first-class Codex setup to pbi-cli.

It installs the bundled Power BI skills into Codex's agent skill directory:

```text
~/.agents/skills/power-bi-*
```

It also adds a global routing block to:

```text
~/.codex/AGENTS.md
```

## Windows

Windows is the recommended environment for semantic model work because Power BI
Desktop is a Windows application.

```powershell
git clone https://github.com/Juanxchito/pbi-cli-codex.git
cd pbi-cli-codex
powershell -ExecutionPolicy Bypass -File .\scripts\codex\install-codex-windows.ps1
```

Then open Power BI Desktop with a `.pbix` file and run:

```powershell
pbi connect
```

After that, start a new Codex session and ask for Power BI work in natural
language.

## macOS

macOS can use the Codex skills and the PBIR/report-file commands. Semantic
model commands that talk to Power BI Desktop require Windows, a VM, or another
compatible host.

```bash
git clone https://github.com/Juanxchito/pbi-cli-codex.git
cd pbi-cli-codex
bash scripts/codex/install-codex-macos.sh
```

## Verify

```bash
pbi-cli skills list --agent codex
pbi --json setup --info
```

You should see 13 installed `power-bi-*` skills.

## Update

Pull the latest repo changes and re-run the installer:

```bash
git pull
pbi-cli skills install --agent codex --force --yes
```

On Windows, use the PowerShell installer again if the `pbi` executable itself
needs to be updated.
