@echo off
setlocal EnableExtensions

set "ROOT=C:\Users\EmpressAlae\Documents\ffh6"
set "DEBUG_DIR=%ROOT%\tmp\fh6-debug"
set "PRIMARY_ROUTER_DIR=C:\codex\FH6 Telemetry Router (Not Single File Edition)\FH6 Telemetry Router"
set "PRIMARY_ROUTER_EXE=%PRIMARY_ROUTER_DIR%\FH6_UDPort_Forwarder.exe"
set "PRIMARY_ROUTER_CONFIG=%PRIMARY_ROUTER_DIR%\config.json"
set "PROJECT_ROUTER_DIR=%ROOT%\tools\FH6-Telemetry-Router-release\FH6 Telemetry Router"
set "PROJECT_ROUTER_EXE=%PROJECT_ROUTER_DIR%\FH6_Telemetry_Router.exe"
set "PROJECT_ROUTER_CONFIG=%PROJECT_ROUTER_DIR%\config.json"

set "LAUNCH_LOG=%DEBUG_DIR%\steam-launch.log"
set "FH6_STDOUT=%DEBUG_DIR%\fh6.stdout.log"
set "FH6_STDERR=%DEBUG_DIR%\fh6.stderr.log"
set "ROUTER_STDOUT=%DEBUG_DIR%\router.stdout.log"
set "ROUTER_STDERR=%DEBUG_DIR%\router.stderr.log"

if not exist "%DEBUG_DIR%" mkdir "%DEBUG_DIR%" >nul 2>&1

>>"%LAUNCH_LOG%" echo.
>>"%LAUNCH_LOG%" echo [%DATE% %TIME%] FH6 debug launch wrapper invoked.
>>"%LAUNCH_LOG%" echo Original command: %*

if "%~1"=="" (
    >>"%LAUNCH_LOG%" echo No Steam %%command%% was supplied.
    exit /b 2
)

set "GAME_DIR=%~dp1"
set "ROUTER_EXE=%PRIMARY_ROUTER_EXE%"
set "ROUTER_DIR=%PRIMARY_ROUTER_DIR%"

>>"%LAUNCH_LOG%" echo Sanitizing router configs.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$paths=@($env:PRIMARY_ROUTER_CONFIG,$env:PROJECT_ROUTER_CONFIG); foreach($p in $paths){ if(Test-Path -LiteralPath $p){ $c=Get-Content -Raw -LiteralPath $p | ConvertFrom-Json; $c.ForzaPort=5310; $c.GameExeName='forzahorizon6'; $c.AutoWatch=$true; $c.TargetPorts=@(5311); $c.ExePaths=@(); $c | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $p -Encoding UTF8; Write-Output ('Sanitized ' + $p) } }" >>"%LAUNCH_LOG%" 2>&1

>>"%LAUNCH_LOG%" echo Stopping any existing telemetry router process before clean start.
taskkill /IM FH6_UDPort_Forwarder.exe /F >nul 2>&1
taskkill /IM FH6_Telemetry_Router.exe /F >nul 2>&1

if not exist "%ROUTER_EXE%" (
    set "ROUTER_EXE=%PROJECT_ROUTER_EXE%"
    set "ROUTER_DIR=%PROJECT_ROUTER_DIR%"
)

if exist "%ROUTER_EXE%" (
    >>"%LAUNCH_LOG%" echo Starting router: "%ROUTER_EXE%"
    start "FH6 telemetry router" /D "%ROUTER_DIR%" "%ROUTER_EXE%" >>"%ROUTER_STDOUT%" 2>>"%ROUTER_STDERR%"
) else (
    >>"%LAUNCH_LOG%" echo Router executable not found.
)

>>"%LAUNCH_LOG%" echo Starting game from: "%GAME_DIR%"
%* >>"%FH6_STDOUT%" 2>>"%FH6_STDERR%"
set "EXIT_CODE=%ERRORLEVEL%"
>>"%LAUNCH_LOG%" echo [%DATE% %TIME%] Game command exited with code %EXIT_CODE%.

if exist "%GAME_DIR%fastboot.log" (
    copy /Y "%GAME_DIR%fastboot.log" "%DEBUG_DIR%\fastboot.latest.log" >nul 2>&1
    >>"%LAUNCH_LOG%" echo Copied fastboot.log to "%DEBUG_DIR%\fastboot.latest.log".
)

exit /b %EXIT_CODE%
