param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $TelemetryArgs
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "fh6_telemetry.py"
$candidatePaths = @()

$pythonCommand = Get-Command "python.exe" -ErrorAction SilentlyContinue
if ($pythonCommand) {
    $candidatePaths += $pythonCommand.Source
}

$pyCommand = Get-Command "py.exe" -ErrorAction SilentlyContinue
if ($pyCommand) {
    $candidatePaths += $pyCommand.Source
}

$candidatePaths += Join-Path $HOME ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

function Test-PythonRuntime {
    param([string] $Candidate)

    if ($Candidate -like "*\WindowsApps\python.exe" -or $Candidate -like "*\WindowsApps\python3.exe") {
        return $false
    }

    $oldErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $Candidate --version *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
    finally {
        $ErrorActionPreference = $oldErrorActionPreference
    }
}

foreach ($candidate in ($candidatePaths | Where-Object { $_ } | Select-Object -Unique)) {
    if (-not (Test-Path $candidate)) {
        continue
    }

    if (Test-PythonRuntime $candidate) {
        & $candidate $scriptPath @TelemetryArgs
        exit $LASTEXITCODE
    }
}

Write-Error "No working Python runtime found. Install Python 3 or run through the Codex bundled Python runtime."
exit 1
