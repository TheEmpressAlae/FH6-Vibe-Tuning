param(
    [string] $Label = "miata-drag",
    [double] $Duration = 10,
    [int] $Port = 5311,
    [string] $OutputDir = "telemetry",
    [switch] $NoSummary,
    [switch] $PauseOnComplete
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$safeLabel = ($Label -replace "[^A-Za-z0-9._-]+", "-").Trim("-")
if (-not $safeLabel) {
    $safeLabel = "capture"
}

$durationTag = if ($Duration -eq [math]::Floor($Duration)) {
    "{0}s" -f [int] $Duration
}
else {
    ("{0}s" -f $Duration).Replace(".", "p")
}

Push-Location $repoRoot
try {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $baseName = "$stamp-$safeLabel-$durationTag-fh6-telemetry"
    $jsonl = Join-Path $OutputDir "$baseName.jsonl"
    $listenLog = Join-Path $OutputDir "$baseName.listen.txt"
    $summaryLog = Join-Path $OutputDir "$baseName.summary.txt"
    $latest = Join-Path $OutputDir "latest-fh6-capture.txt"

    "CapturePath=$jsonl`nLabel=$safeLabel`nStarted=$((Get-Date).ToString("o"))" |
        Set-Content -LiteralPath $latest

    Write-Host "FH6 telemetry capture: $durationTag on UDP $Port"
    Write-Host "Output: $jsonl"
    Write-Host "GO"

    & .\tools\fh6_telemetry.ps1 listen `
        --port $Port `
        --duration $Duration `
        --jsonl $jsonl `
        --label "$safeLabel-$durationTag" `
        --summary-every 1 *>&1 |
        Tee-Object -FilePath $listenLog

    $listenExit = $LASTEXITCODE
    if ($listenExit -ne 0) {
        throw "Telemetry listener exited with code $listenExit."
    }

    if (-not $NoSummary) {
        & .\tools\fh6_telemetry.ps1 summary $jsonl *>&1 |
            Tee-Object -FilePath $summaryLog
    }

    Add-Content -LiteralPath $latest -Value "Finished=$((Get-Date).ToString("o"))"
    Add-Content -LiteralPath $latest -Value "ListenLog=$listenLog"
    if (-not $NoSummary) {
        Add-Content -LiteralPath $latest -Value "SummaryLog=$summaryLog"
    }
}
finally {
    Pop-Location
    if ($PauseOnComplete) {
        Write-Host ""
        Read-Host "Capture complete. Press Enter to close"
    }
}
