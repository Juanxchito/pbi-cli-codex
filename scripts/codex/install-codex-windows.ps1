param(
    [switch] $SkipConnect
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Resolve-Path (Join-Path $ScriptDir "..\..")

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Resolve-PbiCli {
    $command = Get-Command "pbi-cli" -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $pipxLauncher = Join-Path $HOME ".local\bin\pbi-cli.exe"
    if (Test-Path $pipxLauncher) {
        return $pipxLauncher
    }

    throw "pbi-cli was installed, but its executable was not found on PATH or at $pipxLauncher."
}

if (-not (Test-Command "py")) {
    throw "Python launcher 'py' was not found. Install Python 3.10+ from python.org first."
}

$pythonVersion = py -3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ([version]$pythonVersion -lt [version]"3.10") {
    throw "Python 3.10+ is required. Found Python $pythonVersion."
}

if (-not (Test-Command "pipx")) {
    Write-Host "pipx was not found. Installing pipx for the current user..."
    py -3 -m pip install --user pipx
    py -3 -m pipx ensurepath
    $userBase = py -3 -m site --user-base
    $env:PATH = "$userBase\Scripts;$env:PATH"
}

pipx install --force "$RootDir"
$pbiCli = Resolve-PbiCli
& $pbiCli skills install --agent codex --force --yes

Write-Host ""
Write-Host "pbi-cli is installed for Codex."
Write-Host "Installed skills: $HOME\.agents\skills\power-bi-*"
Write-Host "Codex guidance:   $HOME\.codex\AGENTS.md"

if (-not $SkipConnect) {
    Write-Host ""
    Write-Host "Open Power BI Desktop with a .pbix file, then run:"
    Write-Host "  pbi connect"
}
