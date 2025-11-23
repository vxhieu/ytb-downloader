@echo off
REM Script chạy Video Snapshot Tool trên WSL (chạy từ Windows)
echo Dang khoi dong Video Snapshot Tool (WSL)...
echo.

REM Lấy đường dẫn hiện tại và chuyển sang WSL path
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

REM Chuyển đổi D:\path thành /mnt/d/path
for /f "tokens=1 delims=:" %%a in ("%CURRENT_DIR%") do set "DRIVE=%%a"
set "DRIVE_LOWER=%DRIVE:~0,1%"
set "WSL_PATH=/mnt/%DRIVE_LOWER%/%CURRENT_DIR:~3%"
set "WSL_PATH=%WSL_PATH:\=/%"

REM Chạy ứng dụng trong WSL
wsl bash -c "cd '%WSL_PATH%' && chmod +x run.sh 2>/dev/null; ./run.sh"

if errorlevel 1 (
    echo.
    echo [ERROR] Khong the chay ung dung!
    echo Vui long chay: install_wsl.bat de cai dat lai
    pause
)
