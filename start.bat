@echo off
cd /d "%~dp0"

if not exist "ink_calculator_env\Scripts\streamlit.exe" (
    echo Installing dependencies...
    python -m venv ink_calculator_env
    ink_calculator_env\Scripts\pip install streamlit pandas
)

ink_calculator_env\Scripts\streamlit.exe run ink_calculator.py
