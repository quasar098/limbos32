@echo off
title LIMBOS32
python3 --version >nul
if "%errorlevel%" NEQ "0" (
    echo Python3 is not installed.
    set py3=0
) else (
    echo Python3 is installed.
    set py3=1
)
python --version >nul
if "%errorlevel%" NEQ "0" (
    echo Python is not installed.
    set py=0
) else (
    echo Python is installed.
    set py=1
)
if "%py3%" == "%py%" (
    if "%py%" == "1" (
        echo Detected both, press M to use python3 or press P to use python.
        choice /N /C "MP"
        if "%errorlevel%"=="1" (
            set py=0
        ) else (
            set py3=0
        )
    )
)
cls
if "%py3%"=="0" (
    if "%py%"=="0" (
        echo Python wasn't found, cannot continue...
        echo Press any key to exit...
        pause >nul
        exit
    ) else (    
        python -m pip install -r requirements.txt
    )
) else (
    python3 -m pip install -r requirements.txt
)
echo Do you want to edit the config?
choice
if "%errorlevel%" == "2" (goto :start)
echo Openning config.json in notepad...
notepad config.json
if "%py%" == "1" (
    echo Edit the line starting with "py" and ending with "python3" to "python".
)
pause

:start
if "%py%" == "1" (
    start "" "python" "server.py"& start "" "python" "spawn-all.py"
) else (
    start "" "python3" "server.py"& start "" "python3" "spawn-all.py"
)
