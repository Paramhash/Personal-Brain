@echo off
rem Daily run of the dlmm-hedge-bot bridge (scheduled task "personal-brain-dlmm-bridge").
rem Read-only on the bot repo. Output is appended to bridges\.state\bridge-run.log (gitignored).
cd /d "%~dp0.."
echo ==== %date% %time% >> bridges\.state\bridge-run.log
".venv\Scripts\python.exe" bridges\dlmm_bridge.py --apply >> bridges\.state\bridge-run.log 2>&1
echo exit %errorlevel% >> bridges\.state\bridge-run.log
