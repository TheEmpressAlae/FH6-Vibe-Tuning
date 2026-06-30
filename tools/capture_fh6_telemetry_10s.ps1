param(
    [string] $Label = "auto",
    [double] $Duration = 10,
    [int] $Port = 5311,
    [string] $OutputDir = "telemetry",
    [switch] $NoSummary,
    [switch] $PauseOnComplete
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function ConvertTo-SafeLabel {
    param([string] $Value)

    $safe = ($Value -replace "[^A-Za-z0-9._-]+", "-").Trim("-")
    if (-not $safe) {
        return "capture"
    }

    return $safe.ToLowerInvariant()
}

function Get-Fh6ClassLabel {
    param($CarClass)

    switch ([int] $CarClass) {
        0 { return "d" }
        1 { return "c" }
        2 { return "b" }
        3 { return "a" }
        4 { return "s1" }
        5 { return "s2" }
        6 { return "r" }
        7 { return "x" }
        default { return "class$CarClass" }
    }
}

function Get-Fh6DrivetrainLabel {
    param($DrivetrainType)

    switch ([int] $DrivetrainType) {
        0 { return "fwd" }
        1 { return "rwd" }
        2 { return "awd" }
        default { return "drive$DrivetrainType" }
    }
}

function Get-Fh6AutoLabel {
    param(
        [string] $CapturePath,
        [string] $FallbackLabel
    )

    if (-not (Test-Path -LiteralPath $CapturePath)) {
        return $FallbackLabel
    }

    $line = Get-Content -LiteralPath $CapturePath -TotalCount 1
    if (-not $line) {
        return $FallbackLabel
    }

    try {
        $row = $line | ConvertFrom-Json
    }
    catch {
        return $FallbackLabel
    }

    if ($null -eq $row.CarOrdinal) {
        return $FallbackLabel
    }

    $knownCars = @{
        1459 = "fh6-chevrolet-bel-air-1957"
        1586 = "fh6-lincoln-continental-1962"
        1045 = "fh6-pontiac-firebird-trans-am-gta-1987"
        3249 = "fh6-formula-drift-117-599-gtb-fiorano-2007"
        3852 = "fh6-honda-beat-1991"
        4197 = "fh6-mazda-mx-5-miata-forza-edition-1994"
    }

    $ordinal = [int] $row.CarOrdinal
    $carSlug = $knownCars[$ordinal]
    if (-not $carSlug) {
        $carSlug = "car-$ordinal"
    }

    $classLabel = Get-Fh6ClassLabel $row.CarClass
    $pi = if ($null -ne $row.CarPerformanceIndex) { [int] $row.CarPerformanceIndex } else { "pi-unknown" }
    $drive = Get-Fh6DrivetrainLabel $row.DrivetrainType

    return ConvertTo-SafeLabel "$carSlug-$classLabel-$pi-$drive"
}

function Update-Fh6JsonlLabel {
    param(
        [string] $CapturePath,
        [string] $NewLabel
    )

    if (-not (Test-Path -LiteralPath $CapturePath)) {
        return
    }

    $tempPath = "$CapturePath.relabel.tmp"
    try {
        Get-Content -LiteralPath $CapturePath | ForEach-Object {
            if ($_) {
                try {
                    $row = $_ | ConvertFrom-Json
                    $row._label = $NewLabel
                    $row | ConvertTo-Json -Compress -Depth 8
                }
                catch {
                    $_
                }
            }
        } | Set-Content -LiteralPath $tempPath

        Move-Item -LiteralPath $tempPath -Destination $CapturePath -Force
    }
    finally {
        if (Test-Path -LiteralPath $tempPath) {
            Remove-Item -LiteralPath $tempPath -Force
        }
    }
}

function Get-AvailableBaseName {
    param(
        [string] $Directory,
        [string] $BaseName,
        [string[]] $Extensions
    )

    for ($i = 0; $i -lt 1000; $i++) {
        $candidate = if ($i -eq 0) { $BaseName } else { "{0}-{1}" -f $BaseName, $i }
        $exists = $false
        foreach ($extension in $Extensions) {
            if (Test-Path -LiteralPath (Join-Path $Directory "$candidate$extension")) {
                $exists = $true
                break
            }
        }

        if (-not $exists) {
            return $candidate
        }
    }

    throw "Could not find an available base name for $BaseName."
}

function Format-LatestPath {
    param([string] $Path)

    return $Path.Replace("\", "/")
}

function Get-Fh6ActivePacketCount {
    param([string] $CapturePath)

    if (-not (Test-Path -LiteralPath $CapturePath)) {
        return 0
    }

    return (Select-String `
            -LiteralPath $CapturePath `
            -Pattern '"IsRaceOn"\s*:\s*1(?=[,}])' |
        Measure-Object).Count
}

$labelWasAuto = (-not $PSBoundParameters.ContainsKey("Label")) -or ($Label -eq "") -or ($Label -eq "auto")
$safeLabel = if ($labelWasAuto) { "capture" } else { ConvertTo-SafeLabel $Label }
$startedAt = (Get-Date).ToString("o")
$captureExtensions = @(".jsonl", ".listen.txt", ".summary.txt")

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
    $baseName = Get-AvailableBaseName `
        -Directory $OutputDir `
        -BaseName "$stamp-$safeLabel-$durationTag-fh6-telemetry" `
        -Extensions $captureExtensions
    $jsonl = Join-Path $OutputDir "$baseName.jsonl"
    $listenLog = Join-Path $OutputDir "$baseName.listen.txt"
    $summaryLog = Join-Path $OutputDir "$baseName.summary.txt"
    $latest = Join-Path $OutputDir "latest-fh6-capture.txt"
    $latestGood = Join-Path $OutputDir "latest-good-fh6-capture.txt"

    "CapturePath=$(Format-LatestPath $jsonl)`nLabel=$safeLabel`nLabelMode=$(if ($labelWasAuto) { "auto" } else { "explicit" })`nStarted=$startedAt" |
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

    $packetCount = if (Test-Path -LiteralPath $jsonl) {
        (Get-Content -LiteralPath $jsonl | Measure-Object -Line).Lines
    }
    else {
        0
    }
    $activePacketCount = Get-Fh6ActivePacketCount -CapturePath $jsonl

    if ($packetCount -le 0) {
        "CapturePath=$(Format-LatestPath $jsonl)`nLabel=$safeLabel`nLabelMode=$(if ($labelWasAuto) { "auto" } else { "explicit" })`nStatus=error`nError=NoPackets`nPacketCount=0`nActivePacketCount=0`nStarted=$startedAt`nFinished=$((Get-Date).ToString("o"))`nListenLog=$(Format-LatestPath $listenLog)" |
            Set-Content -LiteralPath $latest
        throw "No telemetry packets were captured on UDP $Port."
    }

    if ($labelWasAuto) {
        $autoLabel = Get-Fh6AutoLabel -CapturePath $jsonl -FallbackLabel $safeLabel
        if ($autoLabel -and ($autoLabel -ne $safeLabel)) {
            $oldJsonl = $jsonl
            $oldListenLog = $listenLog
            $safeLabel = $autoLabel
            $baseName = Get-AvailableBaseName `
                -Directory $OutputDir `
                -BaseName "$stamp-$safeLabel-$durationTag-fh6-telemetry" `
                -Extensions $captureExtensions
            $jsonl = Join-Path $OutputDir "$baseName.jsonl"
            $listenLog = Join-Path $OutputDir "$baseName.listen.txt"

            Move-Item -LiteralPath $oldJsonl -Destination $jsonl
            Move-Item -LiteralPath $oldListenLog -Destination $listenLog
            Update-Fh6JsonlLabel -CapturePath $jsonl -NewLabel "$safeLabel-$durationTag"
            Write-Host "Auto label: $safeLabel"
            Write-Host "Renamed output: $jsonl"
        }
    }

    $summaryLog = Join-Path $OutputDir "$baseName.summary.txt"
    if (-not $NoSummary) {
        & .\tools\fh6_telemetry.ps1 summary $jsonl *>&1 |
            Tee-Object -FilePath $summaryLog
        $summaryExit = $LASTEXITCODE
        if ($summaryExit -ne 0) {
            "CapturePath=$(Format-LatestPath $jsonl)`nLabel=$safeLabel`nLabelMode=$(if ($labelWasAuto) { "auto" } else { "explicit" })`nStatus=error`nError=SummaryFailed`nSummaryExitCode=$summaryExit`nPacketCount=$packetCount`nActivePacketCount=$activePacketCount`nStarted=$startedAt`nFinished=$((Get-Date).ToString("o"))`nListenLog=$(Format-LatestPath $listenLog)`nSummaryLog=$(Format-LatestPath $summaryLog)" |
                Set-Content -LiteralPath $latest
            throw "Telemetry summary exited with code $summaryExit."
        }
    }

    "CapturePath=$(Format-LatestPath $jsonl)`nLabel=$safeLabel`nLabelMode=$(if ($labelWasAuto) { "auto" } else { "explicit" })`nStatus=complete`nPacketCount=$packetCount`nActivePacketCount=$activePacketCount`nStarted=$startedAt`nFinished=$((Get-Date).ToString("o"))`nListenLog=$(Format-LatestPath $listenLog)" |
        Set-Content -LiteralPath $latest
    if (-not $NoSummary) {
        Add-Content -LiteralPath $latest -Value "SummaryLog=$(Format-LatestPath $summaryLog)"
    }
    if ($activePacketCount -gt 0) {
        $latestGoodContent = Get-Content -LiteralPath $latest -Raw
        Set-Content -LiteralPath $latestGood -Value $latestGoodContent
    }
    else {
        Add-Content -LiteralPath $latest -Value "LatestGoodUpdate=skipped_no_active_packets"
    }
}
finally {
    Pop-Location
    if ($PauseOnComplete) {
        Write-Host ""
        Read-Host "Capture complete. Press Enter to close"
    }
}
