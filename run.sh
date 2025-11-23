#!/bin/bash
# Script chạy Video Snapshot Tool trên Linux/WSL
# Có thể chạy trực tiếp trong WSL hoặc từ Windows qua: wsl run.sh

# Kiểm tra virtual environment
if [ -d "venv" ]; then
    echo "Đang kích hoạt virtual environment..."
    source venv/bin/activate
fi

# Chạy ứng dụng
echo "Đang khởi động Video Snapshot Tool..."
echo ""

if [ -d "venv" ]; then
    python video_snapshot_tool.py
else
    python3 video_snapshot_tool.py
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Không thể chạy ứng dụng!"
    echo "Vui lòng chạy: ./install.sh để cài đặt lại"
fi


