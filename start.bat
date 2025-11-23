@echo off
REM Script launcher thông minh - Tự động phát hiện và chạy Video Snapshot Tool
REM Chỉ cần double-click file này để chạy ứng dụng

echo ========================================
echo Video Snapshot Tool - Launcher
echo ========================================
echo.

REM Kiểm tra xem có WSL không
where wsl >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] WSL detected. Using WSL mode...
    echo.
    
    REM Lấy đường dẫn hiện tại và chuyển sang WSL path
    set "CURRENT_DIR=%~dp0"
    set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"
    
    REM Chuyển đổi D:\path thành /mnt/d/path
    for /f "tokens=1 delims=:" %%a in ("%CURRENT_DIR%") do set "DRIVE=%%a"
    set "DRIVE_LOWER=%DRIVE:~0,1%"
    set "WSL_PATH=/mnt/%DRIVE_LOWER%/%CURRENT_DIR:~3%"
    set "WSL_PATH=%WSL_PATH:\=/%"
    
    REM Kiểm tra xem đã cài đặt thư viện chưa
    wsl bash -c "cd '%WSL_PATH%' && (test -d venv && source venv/bin/activate && python -c 'import cv2, PIL' 2>/dev/null || python3 -c 'import cv2, PIL' 2>/dev/null)" >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Chua cai dat thu vien. Dang cai dat tu dong...
        echo.
        call install_wsl.bat
        if errorlevel 1 (
            echo [ERROR] Cai dat that bai!
            pause
            exit /b 1
        )
    )
    
    REM Chạy ứng dụng trong WSL
    echo [INFO] Dang khoi dong ung dung...
    echo.
    wsl bash -c "cd '%WSL_PATH%' && if [ -d 'venv' ]; then source venv/bin/activate && python video_snapshot_tool.py; else python3 video_snapshot_tool.py; fi"
    
) else (
    echo [INFO] Windows Native mode...
    echo.
    
    REM Kiểm tra Python
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python chua duoc cai dat!
        echo Vui long cai dat Python 3.8+ tu https://www.python.org/
        echo.
        echo Hoac cai dat WSL de su dung che do WSL.
        pause
        exit /b 1
    )
    
    REM Kiểm tra xem đã cài đặt thư viện chưa
    python -c "import cv2; import PIL" >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Chua cai dat thu vien. Dang cai dat tu dong...
        echo.
        call install.bat
        if errorlevel 1 (
            echo [ERROR] Cai dat that bai!
            pause
            exit /b 1
        )
    )
    
    REM Chạy ứng dụng
    echo [INFO] Dang khoi dong ung dung...
    echo.
    python video_snapshot_tool.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Khong the chay ung dung!
    pause
    exit /b 1
)

exit /b 0
