$ErrorActionPreference = "Stop"

$version = "v1.0.2"
$assetName = "FH6_Telemetry_Router_v1.0.2.zip"
$assetUrl = "https://github.com/Kurinshiku34/FH6-UDP-Telemetry-Router/releases/download/$version/$assetName"
$zipPath = Join-Path $PSScriptRoot $assetName
$releaseDir = Join-Path $PSScriptRoot "FH6-Telemetry-Router-release"

Invoke-WebRequest -UseBasicParsing -Uri $assetUrl -OutFile $zipPath
New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $releaseDir -Force

Get-FileHash -Algorithm SHA256 $zipPath
Get-FileHash -Algorithm SHA256 (Join-Path $releaseDir "FH6 Telemetry Router\FH6_Telemetry_Router.exe")
