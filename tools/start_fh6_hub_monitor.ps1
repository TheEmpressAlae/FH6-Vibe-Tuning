[CmdletBinding()]
param(
    [int]$DurationMinutes = 30,
    [int]$SampleSeconds = 5,
    [switch]$StartGame,
    [switch]$NoStartHub,
    [switch]$EnableLocalDumps,
    [string]$RouterExe = "",
    [string]$LogRoot = ""
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
if (-not $LogRoot) {
    $LogRoot = Join-Path $root "tmp\fh6-hub-monitor"
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logDir = Join-Path $LogRoot $stamp
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$transcript = Join-Path $logDir "transcript.log"
try {
    Start-Transcript -LiteralPath $transcript -Force | Out-Null
} catch {
    Write-Warning "Could not start transcript: $($_.Exception.Message)"
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "=== $Title ==="
}

function Resolve-RouterExe {
    param([string]$Override)

    if ($Override) {
        if (-not (Test-Path -LiteralPath $Override)) {
            throw "Router executable not found: $Override"
        }
        return (Resolve-Path -LiteralPath $Override).Path
    }

    $candidates = @(
        "C:\codex\FH6 Telemetry Router (Not Single File Edition)\FH6 Telemetry Router\FH6_UDPort_Forwarder.exe",
        (Join-Path $PSScriptRoot "FH6-Telemetry-Router-release\FH6 Telemetry Router\FH6_Telemetry_Router.exe")
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    throw "No FH6 telemetry hub/router executable found."
}

function Set-RouterConfig {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $config = [ordered]@{
        ForzaPort = 5310
        GameExeName = "forzahorizon6"
        AutoWatch = $true
        TargetPorts = @(5311)
        ExePaths = @()
    }

    $config | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Path -Encoding UTF8
    Write-Host "Sanitized $Path"
}

function Get-InterestingProcesses {
    Get-Process -ErrorAction SilentlyContinue |
        Where-Object {
            $_.ProcessName -match "forzahorizon6|Forza|Telemetry|UDPort|Forwarder|Router|Hub|Splitter|ForzaDash|ForzaTuner|ONYX" -or
            ($_.Path -and $_.Path -match "ForzaHorizon6|Telemetry|UDPort|Router|Hub|Splitter|ForzaDash|ForzaTuner|ONYX")
        } |
        Sort-Object ProcessName, Id
}

function Get-TelemetryPorts {
    $ports = @(5607, 8000, 1234, 5310, 5311)
    Get-NetUDPEndpoint -ErrorAction SilentlyContinue |
        Where-Object { $_.LocalPort -in $ports } |
        Sort-Object LocalPort
}

function Enable-LocalDumpForExe {
    param(
        [string]$ExeName,
        [string]$DumpDir
    )

    $key = "HKCU:\Software\Microsoft\Windows\Windows Error Reporting\LocalDumps\$ExeName"
    New-Item -Path $key -Force | Out-Null
    New-ItemProperty -Path $key -Name DumpFolder -Value $DumpDir -PropertyType ExpandString -Force | Out-Null
    New-ItemProperty -Path $key -Name DumpCount -Value 5 -PropertyType DWord -Force | Out-Null
    New-ItemProperty -Path $key -Name DumpType -Value 2 -PropertyType DWord -Force | Out-Null
    Write-Host "Enabled WER local dumps for $ExeName -> $DumpDir"
}

$startedAt = Get-Date
$routerExePath = Resolve-RouterExe -Override $RouterExe
$routerDir = Split-Path -Parent $routerExePath
$routerName = [IO.Path]::GetFileNameWithoutExtension($routerExePath)
$routerExeName = [IO.Path]::GetFileName($routerExePath)

Write-Section "FH6 hub monitor"
Write-Host "Started: $($startedAt.ToString("o"))"
Write-Host "Log directory: $logDir"
Write-Host "Router executable: $routerExePath"
Write-Host "Duration minutes: $DurationMinutes"
Write-Host "Sample seconds: $SampleSeconds"

Write-Section "Sanitize router configs"
$configPaths = @(
    "C:\codex\FH6 Telemetry Router (Not Single File Edition)\FH6 Telemetry Router\config.json",
    (Join-Path $PSScriptRoot "FH6-Telemetry-Router-release\FH6 Telemetry Router\config.json")
)
foreach ($configPath in $configPaths) {
    Set-RouterConfig -Path $configPath
}

if ($EnableLocalDumps) {
    Write-Section "Enable WER LocalDumps"
    $dumpDir = Join-Path $logDir "dumps"
    New-Item -ItemType Directory -Force -Path $dumpDir | Out-Null
    Enable-LocalDumpForExe -ExeName "forzahorizon6.exe" -DumpDir $dumpDir
    Enable-LocalDumpForExe -ExeName $routerExeName -DumpDir $dumpDir
}

Write-Section "Preflight processes"
Get-InterestingProcesses | Select-Object ProcessName, Id, CPU, WorkingSet64, StartTime, Path | Format-Table -AutoSize -Wrap

Write-Section "Preflight UDP endpoints"
$prePorts = Get-TelemetryPorts
if ($prePorts) {
    $prePorts | ForEach-Object {
        $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
        [PSCustomObject]@{
            LocalAddress = $_.LocalAddress
            LocalPort = $_.LocalPort
            PID = $_.OwningProcess
            Process = $proc.ProcessName
            Path = $proc.Path
        }
    } | Format-Table -AutoSize -Wrap
} else {
    Write-Host "No telemetry UDP endpoints are currently bound."
}

if ($StartGame) {
    Write-Section "Start FH6 through Steam"
    Start-Process "steam://rungameid/2483190"
    Write-Host "Started Steam URI steam://rungameid/2483190"
    Start-Sleep -Seconds 20
}

$hubProcess = $null
if (-not $NoStartHub) {
    Write-Section "Start hub/router"
    $stdout = Join-Path $logDir "hub.stdout.log"
    $stderr = Join-Path $logDir "hub.stderr.log"
    $corehostTrace = Join-Path $logDir "hub.corehost-trace.log"

    $oldCorehostTrace = $env:COREHOST_TRACE
    $oldCorehostTraceFile = $env:COREHOST_TRACEFILE
    $env:COREHOST_TRACE = "1"
    $env:COREHOST_TRACEFILE = $corehostTrace

    try {
        $hubProcess = Start-Process -FilePath $routerExePath `
            -WorkingDirectory $routerDir `
            -RedirectStandardOutput $stdout `
            -RedirectStandardError $stderr `
            -PassThru
    } finally {
        if ($null -eq $oldCorehostTrace) {
            Remove-Item Env:\COREHOST_TRACE -ErrorAction SilentlyContinue
        } else {
            $env:COREHOST_TRACE = $oldCorehostTrace
        }

        if ($null -eq $oldCorehostTraceFile) {
            Remove-Item Env:\COREHOST_TRACEFILE -ErrorAction SilentlyContinue
        } else {
            $env:COREHOST_TRACEFILE = $oldCorehostTraceFile
        }
    }

    Write-Host "Hub/router PID: $($hubProcess.Id)"
    Write-Host "stdout: $stdout"
    Write-Host "stderr: $stderr"
    Write-Host "corehost trace: $corehostTrace"
}

$samplePath = Join-Path $logDir "process-samples.csv"
$portPath = Join-Path $logDir "udp-endpoints.csv"
$deadline = (Get-Date).AddMinutes($DurationMinutes)
$gameWasSeen = $false
$hubWasSeen = $false

Write-Section "Monitor loop"
Write-Host "Monitoring until $($deadline.ToString("o")). Press Ctrl+C to stop early."

while ((Get-Date) -lt $deadline) {
    $now = Get-Date
    $interesting = Get-InterestingProcesses
    $fh6 = $interesting | Where-Object { $_.ProcessName -eq "forzahorizon6" } | Select-Object -First 1
    $hub = $null
    if ($hubProcess) {
        $hub = Get-Process -Id $hubProcess.Id -ErrorAction SilentlyContinue
    } else {
        $hub = $interesting | Where-Object { $_.ProcessName -eq $routerName } | Select-Object -First 1
    }

    if ($fh6) { $gameWasSeen = $true }
    if ($hub) { $hubWasSeen = $true }

    foreach ($proc in $interesting) {
        [PSCustomObject]@{
            Time = $now.ToString("o")
            ProcessName = $proc.ProcessName
            PID = $proc.Id
            CPU = $proc.CPU
            WorkingSetMB = [math]::Round($proc.WorkingSet64 / 1MB, 1)
            PrivateMemoryMB = [math]::Round($proc.PrivateMemorySize64 / 1MB, 1)
            Path = $proc.Path
        } | Export-Csv -LiteralPath $samplePath -NoTypeInformation -Append
    }

    $portsNow = Get-TelemetryPorts
    if ($portsNow) {
        foreach ($endpoint in $portsNow) {
            $proc = Get-Process -Id $endpoint.OwningProcess -ErrorAction SilentlyContinue
            [PSCustomObject]@{
                Time = $now.ToString("o")
                LocalAddress = $endpoint.LocalAddress
                LocalPort = $endpoint.LocalPort
                PID = $endpoint.OwningProcess
                ProcessName = $proc.ProcessName
                Path = $proc.Path
            } | Export-Csv -LiteralPath $portPath -NoTypeInformation -Append
        }
    } else {
        [PSCustomObject]@{
            Time = $now.ToString("o")
            LocalAddress = ""
            LocalPort = ""
            PID = ""
            ProcessName = "none"
            Path = ""
        } | Export-Csv -LiteralPath $portPath -NoTypeInformation -Append
    }

    if ($gameWasSeen -and -not $fh6) {
        Write-Warning "FH6 process disappeared at $($now.ToString("o"))."
        break
    }

    if ($hubWasSeen -and -not $hub) {
        Write-Warning "Hub/router process disappeared at $($now.ToString("o"))."
        break
    }

    Start-Sleep -Seconds $SampleSeconds
}

Write-Section "Postflight event logs"
$eventPath = Join-Path $logDir "application-events.txt"
Get-WinEvent -FilterHashtable @{ LogName = "Application"; StartTime = $startedAt } -ErrorAction SilentlyContinue |
    Where-Object {
        $_.ProviderName -match "Application Error|Windows Error Reporting|.NET Runtime" -or
        $_.Message -match "forzahorizon6|ForzaHorizon6|FH6|Telemetry|UDPort|Router|$([regex]::Escape($routerExeName))"
    } |
    Select-Object TimeCreated, ProviderName, Id, LevelDisplayName, @{ Name = "Message"; Expression = { $_.Message -replace "`r?`n", " " } } |
    Format-List |
    Out-File -LiteralPath $eventPath -Encoding UTF8
Write-Host "Wrote $eventPath"

Write-Section "Copy Steam and fastboot context"
$steamGameProcess = "C:\Program Files (x86)\Steam\logs\gameprocess_log.txt"
if (Test-Path -LiteralPath $steamGameProcess) {
    Get-Content -LiteralPath $steamGameProcess -Tail 250 |
        Set-Content -LiteralPath (Join-Path $logDir "steam-gameprocess-tail.log") -Encoding UTF8
}

$fastboot = "C:\Program Files (x86)\Steam\steamapps\common\ForzaHorizon6\fastboot.log"
if (Test-Path -LiteralPath $fastboot) {
    Copy-Item -LiteralPath $fastboot -Destination (Join-Path $logDir "fastboot.latest.log") -Force
}

if ($hubProcess) {
    $hubProcess.Refresh()
    if ($hubProcess.HasExited) {
        Write-Host "Hub/router exited with code $($hubProcess.ExitCode)."
    } else {
        Write-Host "Hub/router still running with PID $($hubProcess.Id)."
    }
}

Write-Host "Monitor artifacts: $logDir"

try {
    Stop-Transcript | Out-Null
} catch {
}
