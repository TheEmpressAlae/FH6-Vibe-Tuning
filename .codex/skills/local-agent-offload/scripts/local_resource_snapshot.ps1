[CmdletBinding()]
param(
    [string]$NameRegex = 'Codex|codex|node_repl|powershell|pwsh|python|node|git|rg|npm|dotnet|cargo|forzahorizon|FH6|Steam',
    [int]$SampleMs = 1500,
    [int]$Top = 30
)

$ErrorActionPreference = 'SilentlyContinue'

function Convert-ToGB {
    param($Kb)
    if ($null -eq $Kb) { return $null }
    return [math]::Round($Kb / 1MB, 2)
}

function Convert-BytesToMB {
    param($Bytes)
    if ($null -eq $Bytes) { return $null }
    return [math]::Round($Bytes / 1MB, 1)
}

function Get-MatchingProcesses {
    Get-Process | Where-Object { $_.ProcessName -match $NameRegex } |
        Select-Object Id, ProcessName, CPU, WorkingSet64, PrivateMemorySize64, StartTime, Path
}

$first = @(Get-MatchingProcesses)
Start-Sleep -Milliseconds $SampleMs
$second = @(Get-MatchingProcesses)

$firstById = @{}
foreach ($process in $first) {
    $firstById[$process.Id] = $process
}

$processRows = foreach ($process in $second) {
    $old = $firstById[$process.Id]
    $cpuPctOneCore = $null
    if ($old -and $null -ne $process.CPU -and $null -ne $old.CPU -and $SampleMs -gt 0) {
        $cpuPctOneCore = [math]::Round((($process.CPU - $old.CPU) / ($SampleMs / 1000.0)) * 100, 1)
    }

    [pscustomobject]@{
        processName = $process.ProcessName
        id = $process.Id
        cpuPctOneCore = $cpuPctOneCore
        workingSetMB = Convert-BytesToMB $process.WorkingSet64
        privateMB = Convert-BytesToMB $process.PrivateMemorySize64
        startTime = if ($process.StartTime) { $process.StartTime.ToString('o') } else { $null }
        path = $process.Path
    }
}

$cpuLoadPct = $null
$memory = $null

try {
    $cpuLoadPct = [math]::Round((Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average, 1)
} catch {}

try {
    $os = Get-CimInstance Win32_OperatingSystem
    $memory = [pscustomobject]@{
        totalGB = Convert-ToGB $os.TotalVisibleMemorySize
        freeGB = Convert-ToGB $os.FreePhysicalMemory
        usedPct = if ($os.TotalVisibleMemorySize -gt 0) {
            [math]::Round((1 - ($os.FreePhysicalMemory / $os.TotalVisibleMemorySize)) * 100, 1)
        } else {
            $null
        }
    }
} catch {}

[pscustomobject]@{
    capturedAt = (Get-Date).ToString('o')
    sampleMs = $SampleMs
    cpuLoadPct = $cpuLoadPct
    memory = $memory
    matchedProcessRegex = $NameRegex
    processes = @($processRows | Sort-Object cpuPctOneCore -Descending | Select-Object -First $Top)
} | ConvertTo-Json -Depth 5

