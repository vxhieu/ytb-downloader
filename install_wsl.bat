@echo off
REM Script cài đặt Video Snapshot Tool cho WSL (chạy từ Windows)
echo ========================================
echo Video Snapshot Tool - Cài đặt (WSL)
echo ========================================
echo.

REM Lấy đường dẫn hiện tại và chuyển sang WSL path
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

REM Chuyển đổi D:\path thành /mnt/d/path
for /f "tokens=1 delims=:" %%a in ("%CURRENT_DIR%") do set "DRIVE=%%a"
set "DRIVE_LOWER=%DRIVE:~0,1%"
set "WSL_PATH=/mnt/%DRIVE_LOWER%/%CURRENT_DIR:~3%"
set "WSL_PATH=%WSL_PATH:\=/%"

echo [INFO] Duong dan WSL: %WSL_PATH%
echo.

REM Chạy script install.sh trong WSL
echo [INFO] Dang chay script cai dat trong WSL...
echo.
wsl bash -c "cd '%WSL_PATH%' && chmod +x install.sh 2>/dev/null; ./install.sh"

if errorlevel 1 (
    echo.
    echo [ERROR] Cai dat that bai!
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Cai dat thanh cong!
echo ========================================
echo.
echo De chay ung dung, su dung lenh:
echo   wsl run_wsl.bat
echo.
echo Hoac chay file: run_wsl.bat
echo.
pause

