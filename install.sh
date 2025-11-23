#!/bin/bash
# Script cài đặt Video Snapshot Tool cho Linux/WSL
# Có thể chạy trực tiếp trong WSL hoặc từ Windows qua: wsl install.sh

echo "========================================"
echo "Video Snapshot Tool - Cài đặt (WSL/Linux)"
echo "========================================"
echo ""

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 chưa được cài đặt!${NC}"
    echo "Vui lòng cài đặt Python 3.8+ bằng lệnh:"
    echo "  sudo apt update && sudo apt install python3 python3-pip -y"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}[OK] Python đã được cài đặt: $PYTHON_VERSION${NC}"
echo ""

# Kiểm tra pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo -e "${RED}[ERROR] pip chưa được cài đặt!${NC}"
    echo "Vui lòng cài đặt pip bằng lệnh:"
    echo "  sudo apt install python3-pip -y"
    exit 1
fi

echo -e "${GREEN}[OK] pip đã sẵn sàng${NC}"
echo ""

# Kiểm tra xem có cần venv không (Python 3.12+ hoặc Ubuntu 23.04+)
NEED_VENV=false
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 12 ]; then
    NEED_VENV=true
    echo -e "${YELLOW}[INFO] Python 3.12+ phát hiện, sẽ sử dụng virtual environment${NC}"
    echo ""
fi

# Tạo virtual environment nếu cần
if [ "$NEED_VENV" = true ]; then
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}[INFO] Đang tạo virtual environment...${NC}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERROR] Không thể tạo virtual environment!${NC}"
            echo "Vui lòng cài đặt python3-venv:"
            echo "  sudo apt install python3-venv python3-full -y"
            exit 1
        fi
        echo -e "${GREEN}[OK] Virtual environment đã được tạo${NC}"
    else
        echo -e "${GREEN}[OK] Virtual environment đã tồn tại${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}[INFO] Đang kích hoạt virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}[OK] Virtual environment đã được kích hoạt${NC}"
    echo ""
fi

# Cập nhật pip
echo -e "${YELLOW}[INFO] Đang cập nhật pip...${NC}"
if [ "$NEED_VENV" = true ]; then
    pip install --upgrade pip --quiet
else
    pip3 install --user --upgrade pip --quiet 2>/dev/null || python3 -m pip install --user --upgrade pip --quiet
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK] pip đã được cập nhật${NC}"
else
    echo -e "${YELLOW}[WARNING] Không thể cập nhật pip, tiếp tục...${NC}"
fi
echo ""

# Cài đặt thư viện
echo -e "${YELLOW}[INFO] Đang cài đặt các thư viện cần thiết...${NC}"
echo ""

if [ "$NEED_VENV" = true ]; then
    pip install -r requirements.txt
else
    pip3 install --user -r requirements.txt 2>/dev/null || python3 -m pip install --user -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo -e "${GREEN}[SUCCESS] Cài đặt thành công!${NC}"
    echo "========================================"
    echo ""
    echo -e "${CYAN}Để chạy ứng dụng:${NC}"
    if [ "$NEED_VENV" = true ]; then
        echo "  source venv/bin/activate"
        echo "  python video_snapshot_tool.py"
        echo ""
        echo "Hoặc chạy file: ./run.sh"
    else
        echo "  python3 video_snapshot_tool.py"
        echo ""
        echo "Hoặc chạy file: ./run.sh"
    fi
    echo ""
else
    echo ""
    echo -e "${RED}[ERROR] Cài đặt thất bại!${NC}"
    exit 1
fi


