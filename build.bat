@echo off
setlocal EnableDelayedExpansion

set SCRIPT_NAME=filename-character-renamer-z.py
set APP_NAME=Filename Character Renamer Z
set EXEC_NAME=Filename_Character_Renamer_Z.exe
set ICON_FILE=icon_fcr_z.ico

cd /d "%~dp0"

:: Strip trailing backslash from %%~dp0 to avoid broken quoted paths.
set "PROJ=%~dp0"
set "PROJ=%PROJ:~0,-1%"

echo ===========================================
echo  Building Filename Character Renamer Z
echo  for Windows
echo ===========================================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from python.org and add to PATH.
    pause
    exit /b 1
)

:: Check script exists
if not exist "%SCRIPT_NAME%" (
    echo [ERROR] %SCRIPT_NAME% not found in current directory.
    pause
    exit /b 1
)

:: Install dependencies
echo [INFO] Checking dependencies...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    python -m pip install pyinstaller
)
python -m pip show pillow >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing Pillow...
    python -m pip install pillow
)

:: Clean old builds
echo [INFO] Cleaning old builds...
if exist "%PROJ%\build"       rd /s /q "%PROJ%\build"
if exist "%PROJ%\__pycache__" rd /s /q "%PROJ%\__pycache__"

:: Generate icon
:: Icon is now embedded as base64 directly inside the .py source (single
:: source of truth, also used to set the live window icon at runtime).
:: This just asks the script to export it to a temp .ico file.
echo [INFO] Generating icon...
python "%SCRIPT_NAME%" --generate-icon --ico="%PROJ%\%ICON_FILE%"
if not exist "%PROJ%\%ICON_FILE%" (
    echo [WARN] Icon generation failed, building without icon.
)

:: Build executable
echo [INFO] Building executable...
if exist "%PROJ%\%ICON_FILE%" (
    python -m PyInstaller --onefile --windowed --name "Filename_Character_Renamer_Z" --icon "%PROJ%\%ICON_FILE%" --distpath "%PROJ%" --workpath "%PROJ%\build" --specpath "%PROJ%" "%SCRIPT_NAME%"
) else (
    python -m PyInstaller --onefile --windowed --name "Filename_Character_Renamer_Z" --distpath "%PROJ%" --workpath "%PROJ%\build" --specpath "%PROJ%" "%SCRIPT_NAME%"
)
if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

:: Create Desktop and Start Menu shortcuts via a temp PowerShell script.
:: Writing a .ps1 file avoids ALL cmd.exe quoting/escaping issues that
:: break inline -Command calls when paths contain spaces or special chars.
echo [INFO] Creating shortcuts...
set "PS_TMP=%TEMP%\fcr_z_shortcut_%RANDOM%.ps1"
set "TARGET=%PROJ%\%EXEC_NAME%"
set "STARTMENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU_DIR%" mkdir "%STARTMENU_DIR%"

(
    echo $target   = '%TARGET%'
    echo $workdir  = '%PROJ%'
    echo $appname  = 'Filename Character Renamer Z'
    echo $desc     = 'Filename Character Renamer Z'
    echo $ws = New-Object -ComObject WScript.Shell
    echo.
    echo # Desktop shortcut ^(uses the real shell folder, works on all locales^)
    echo $desktop = [Environment]::GetFolderPath^('Desktop'^)
    echo $lnk1 = $ws.CreateShortcut^("$desktop\$appname.lnk"^)
    echo $lnk1.TargetPath       = $target
    echo $lnk1.WorkingDirectory = $workdir
    echo $lnk1.IconLocation     = "$target,0"
    echo $lnk1.Description      = $desc
    echo $lnk1.Save^(^)
    echo Write-Host "[OK] Desktop shortcut created: $desktop\$appname.lnk"
    echo.
    echo # Start Menu shortcut
    echo $startmenu = '%STARTMENU_DIR%'
    echo $lnk2 = $ws.CreateShortcut^("$startmenu\$appname.lnk"^)
    echo $lnk2.TargetPath       = $target
    echo $lnk2.WorkingDirectory = $workdir
    echo $lnk2.IconLocation     = "$target,0"
    echo $lnk2.Description      = $desc
    echo $lnk2.Save^(^)
    echo Write-Host "[OK] Start Menu shortcut created: $startmenu\$appname.lnk"
) > "%PS_TMP%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_TMP%"
if errorlevel 1 (
    echo [WARN] Shortcut creation may have failed. Check paths manually.
)
del /f /q "%PS_TMP%" >nul 2>&1

:: Clean up build artifacts
echo [INFO] Cleaning up...
del /f /q "%PROJ%\%ICON_FILE%" >nul 2>&1
if exist "%PROJ%\build"                             rd /s /q "%PROJ%\build"
if exist "%PROJ%\Filename_Character_Renamer_Z.spec" del /f /q "%PROJ%\Filename_Character_Renamer_Z.spec"

echo.
echo [OK] Done!
echo    Executable : %PROJ%\%EXEC_NAME%
echo    Desktop    : %USERPROFILE%\Desktop\%APP_NAME%.lnk
echo    Start Menu : %STARTMENU_DIR%\%APP_NAME%.lnk
pause
exit /b 0
