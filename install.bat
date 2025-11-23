@echo off
REM Script cài đặt Video Snapshot Tool cho Windows (Native)
REM Nếu bạn dùng WSL, hãy chạy install_wsl.bat thay vì file này
echo ========================================
echo Video Snapshot Tool - Cài đặt (Windows Native)
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai dat Python 3.8+ tu https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python da duoc cai dat
python --version
echo.

REM Kiểm tra pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip chua duoc cai dat!
    pause
    exit /b 1
)

echo [OK] pip da san sang
echo.

REM Cập nhật pip
echo [INFO] Dang cap nhat pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip da duoc cap nhat
echo.

REM Cài đặt thư viện
echo [INFO] Dang cai dat cac thu vien can thiet...
echo.
python -m pip install -r requirements.txt
if errorlevel 1 (
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
echo   python video_snapshot_tool.py
echo.
echo Hoac chay file: run.bat
echo.
pause


