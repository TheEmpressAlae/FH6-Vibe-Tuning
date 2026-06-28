$ErrorActionPreference = "Stop"

$routerExe = Join-Path $PSScriptRoot "FH6-Telemetry-Router-release\FH6 Telemetry Router\FH6_Telemetry_Router.exe"

if (-not (Test-Path $routerExe)) {
    Write-Error "Router executable not found. Run .\tools\download_fh6_router_release.ps1 first."
    exit 1
}

# Keep this as one physical line when pasting into Steam Launch Options.
Write-Output ('cmd /c start "" "{0}" && %command%' -f $routerExe)
