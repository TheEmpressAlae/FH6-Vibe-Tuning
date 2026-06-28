$ErrorActionPreference = "Stop"

$routerDir = Join-Path $PSScriptRoot "FH6-Telemetry-Router-release\FH6 Telemetry Router"
$configPath = Join-Path $routerDir "config.json"

if (-not (Test-Path $routerDir)) {
    Write-Error "Router release folder not found. Run .\tools\download_fh6_router_release.ps1 first."
    exit 1
}

$config = [ordered]@{
    ForzaPort = 5310
    GameExeName = "forzahorizon6"
    AutoWatch = $true
    TargetPorts = @(5311)
    ExePaths = @()
}

$config | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $configPath -Encoding UTF8
Write-Host "Wrote $configPath"
