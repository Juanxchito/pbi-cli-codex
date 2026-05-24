# pbi-cli for Codex

This repository is a Codex-focused adaptation of Mina Saad's original
[`MinaSaad1/pbi-cli`](https://github.com/MinaSaad1/pbi-cli). The upstream
project provides the core Power BI CLI, Power BI Desktop interop, PBIR report
commands, and original Power BI agent skills. This fork adds first-class Codex
setup on top of that work.

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

### Windows SSPI / Codex Sandbox Note

On Windows, `pbi connect` may auto-detect the correct Power BI Desktop
localhost port but still fail inside a sandboxed Codex command with an SSPI
authentication error such as:

```text
No hay credenciales disponibles en el paquete de seguridad
```

or:

```text
No credentials are available in the security package
```

If the same command works outside the sandbox, the PBIX file, detected port, and
Power BI Desktop instance are probably fine. The failure is caused by the
sandboxed execution context not having access to the Windows integrated
authentication credentials required by the local Analysis Services endpoint.

Recommended action: rerun `pbi connect` outside the sandbox or approve
escalated execution, then continue the Codex workflow.

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
