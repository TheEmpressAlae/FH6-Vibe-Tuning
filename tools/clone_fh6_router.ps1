$ErrorActionPreference = "Stop"

$repoUrl = "https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router.git"
$target = Join-Path $PSScriptRoot "FH6-UDP-Telemetry-Router"

if (Test-Path $target) {
    Write-Host "Router source cache already exists: $target"
    exit 0
}

git clone --depth 1 --branch v1.0.2 $repoUrl $target
