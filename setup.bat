@echo off
cd /d "%~dp0"

python -m venv ink_calculator_env
ink_calculator_env\Scripts\pip install -r requirements.txt

echo.
echo Installation complete. Run start.bat to launch.
pause

