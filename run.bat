@echo off
REM Script chạy Video Snapshot Tool trên Windows (Native)
REM Nếu bạn dùng WSL, hãy chạy run_wsl.bat thay vì file này
echo Dang khoi dong Video Snapshot Tool (Windows Native)...
echo.
python video_snapshot_tool.py
if errorlevel 1 (
    echo.
    echo [ERROR] Khong the chay ung dung!
    echo Vui long chay: install.bat de cai dat lai
    pause
)


