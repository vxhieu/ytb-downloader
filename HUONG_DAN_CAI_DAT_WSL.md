# HƯỚNG DẪN CÀI ĐẶT PYTHON TRONG WSL

## 1. KIỂM TRA WSL ĐÃ CÀI ĐẶT

### Bước 1: Mở WSL Terminal
- Mở **Command Prompt** hoặc **PowerShell** trên Windows
- Gõ lệnh: `wsl` hoặc `bash`
- Hoặc mở **Ubuntu** (hoặc distro Linux khác) từ Start Menu

### Bước 2: Kiểm tra phiên bản WSL
```bash
wsl --version
```

Nếu chưa cài WSL, xem hướng dẫn cài đặt ở cuối tài liệu này.

## 2. CÀI ĐẶT PYTHON

### 2.1. Kiểm tra Python đã có sẵn chưa

```bash
python3 --version
```

hoặc

```bash
python --version
```

Nếu hiển thị phiên bản (ví dụ: `Python 3.10.12`), bạn đã có Python. Chuyển sang bước 3.

### 2.2. Cài đặt Python (nếu chưa có)

#### Ubuntu/Debian:
```bash
# Cập nhật package list
sudo apt update

# Cài đặt Python 3 và pip
sudo apt install python3 python3-pip -y

# Cài đặt các công cụ hỗ trợ
sudo apt install python3-venv python3-dev python3-full -y
```

#### Kiểm tra lại:
```bash
python3 --version
pip3 --version
```

## 3. CÀI ĐẶT THƯ VIỆN CHO VIDEO SNAPSHOT TOOL

### 3.1. Di chuyển đến thư mục project

```bash
# Nếu project ở ổ D: trong Windows
cd /mnt/d/ytb-downloader

# Hoặc nếu project ở thư mục home
cd ~/ytb-downloader
```

### 3.2. Cài đặt thư viện cần thiết

**⚠️ QUAN TRỌNG**: Nếu gặp lỗi "externally-managed-environment", bạn **PHẢI** sử dụng virtual environment (khuyến nghị) hoặc `--break-system-packages` (không khuyến nghị).

#### Cách 1: Sử dụng Virtual Environment (KHUYẾN NGHỊ) ⭐

```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

# Hoặc cài đặt thủ công
pip install opencv-python Pillow
```

**Lưu ý**: Mỗi lần chạy tool, cần kích hoạt virtual environment trước:
```bash
source venv/bin/activate
python video_snapshot_tool.py
```

#### Cách 2: Sử dụng --break-system-packages (KHÔNG KHUYẾN NGHỊ)

Chỉ dùng nếu không muốn dùng virtual environment:

```bash
pip3 install --break-system-packages -r requirements.txt
```

Hoặc:
```bash
pip3 install --break-system-packages opencv-python Pillow
```

⚠️ **Cảnh báo**: Cách này có thể gây conflict với system packages.

### 3.3. Cài đặt dependencies cho OpenCV (nếu cần)

OpenCV có thể cần một số thư viện hệ thống:

```bash
sudo apt update
sudo apt install -y libopencv-dev python3-opencv ffmpeg
sudo apt install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

Nếu vẫn gặp lỗi, thử:

```bash
# Trong venv
pip install opencv-python-headless
```

## 4. KIỂM TRA CÀI ĐẶT

### 4.1. Kiểm tra Python và thư viện

```bash
# Nếu dùng venv, kích hoạt trước
source venv/bin/activate

python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"
python3 -c "from PIL import Image; print('Pillow installed successfully')"
```

### 4.2. Kiểm tra GUI support (Tkinter)

```bash
python3 -c "import tkinter; print('Tkinter available')"
```

Nếu thiếu Tkinter:

```bash
sudo apt install python3-tk -y
```

## 5. CHẠY VIDEO SNAPSHOT TOOL

### 5.1. Chạy trực tiếp

```bash
cd /mnt/d/ytb-downloader

# Nếu dùng venv
source venv/bin/activate

python3 video_snapshot_tool.py
```

### 5.2. Nếu gặp lỗi về display (GUI)

WSL không có display server mặc định. Có 2 cách:

#### Cách 1: Sử dụng X11 Forwarding (khuyến nghị)

**Trên Windows:**
1. Cài đặt **VcXsrv** hoặc **Xming** (X server cho Windows)
   - Download VcXsrv: https://sourceforge.net/projects/vcxsrv/
   - Hoặc Xming: https://sourceforge.net/projects/xming/

2. Chạy X server với các tùy chọn:
   - Display number: 0
   - Start no client: ✓
   - Disable access control: ✓

**Trên WSL:**
```bash
# Thêm vào ~/.bashrc hoặc ~/.zshrc
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

# Hoặc nếu dùng WSL2:
export DISPLAY=$(ip route list default | awk '{print $3}'):0.0

# Load lại
source ~/.bashrc
```

#### Cách 2: Sử dụng WSLg (Windows 11)

Nếu bạn dùng Windows 11, WSLg đã được tích hợp sẵn. Chỉ cần chạy:

```bash
python3 video_snapshot_tool.py
```

### 5.3. Kiểm tra X11 forwarding

```bash
echo $DISPLAY
```

Nếu hiển thị địa chỉ IP, X11 forwarding đã hoạt động.

## 6. TROUBLESHOOTING

### 6.1. Lỗi "externally-managed-environment"

**Giải pháp**: Sử dụng virtual environment (xem mục 3.2 và 9)

```bash
# Tạo và kích hoạt venv
python3 -m venv venv
source venv/bin/activate

# Sau đó cài đặt
pip install -r requirements.txt
```

### 6.2. Lỗi "No module named 'cv2'"

**Nếu đang dùng venv:**
```bash
source venv/bin/activate
pip install --upgrade pip
pip install opencv-python
```

**Nếu không dùng venv:**
```bash
pip3 install --break-system-packages --upgrade pip
pip3 install --break-system-packages opencv-python
```

Nếu vẫn lỗi, thử:

```bash
# Trong venv
pip install opencv-python-headless
```

### 6.3. Lỗi "No display name and no $DISPLAY environment variable"

- Cài đặt X server (VcXsrv hoặc Xming)
- Thiết lập biến môi trường DISPLAY
- Đảm bảo X server đang chạy

### 6.4. Lỗi "cannot connect to X server"

```bash
# Kiểm tra DISPLAY
echo $DISPLAY

# Thử set lại
export DISPLAY=:0.0

# Hoặc với WSL2
export DISPLAY=$(ip route list default | awk '{print $3}'):0.0
```

### 6.5. Lỗi "Tkinter not found"

```bash
sudo apt install python3-tk -y
```

### 6.6. Lỗi về codec video

```bash
sudo apt install ffmpeg libavcodec-dev libavformat-dev libswscale-dev -y
```

## 7. CÀI ĐẶT WSL (NẾU CHƯA CÓ)

### Windows 10/11:

#### Cách 1: Cài đặt tự động (Windows 10 version 2004+ và Windows 11)
```powershell
wsl --install
```

Sau đó restart máy tính.

#### Cách 2: Cài đặt thủ công

1. Mở PowerShell với quyền Administrator
2. Chạy lệnh:
```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
3. Restart máy tính
4. Tải và cài đặt WSL2 kernel update từ Microsoft
5. Đặt WSL2 làm mặc định:
```powershell
wsl --set-default-version 2
```
6. Cài đặt Ubuntu từ Microsoft Store

## 8. TẠO ALIAS ĐỂ DỄ SỬ DỤNG

Thêm vào `~/.bashrc` hoặc `~/.zshrc`:

```bash
# Alias cho video snapshot tool
alias snapshot='cd /mnt/d/ytb-downloader && source venv/bin/activate && python3 video_snapshot_tool.py'
```

Sau đó:
```bash
source ~/.bashrc
```

Bây giờ chỉ cần gõ `snapshot` để chạy tool.

## 9. SỬ DỤNG VIRTUAL ENVIRONMENT (BẮT BUỘC cho Python 3.12+)

**⚠️ Với Python 3.12+ hoặc Ubuntu 23.04+, bạn PHẢI dùng virtual environment!**

Tạo môi trường ảo để tránh conflict và lỗi "externally-managed-environment":

```bash
# Di chuyển đến thư mục project
cd /mnt/d/ytb-downloader

# Tạo virtual environment
python3 -m venv venv

# Kích hoạt
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy tool
python video_snapshot_tool.py

# Thoát virtual environment (khi xong)
deactivate
```

### Tạo alias để dễ sử dụng

Thêm vào `~/.bashrc`:

```bash
# Alias cho video snapshot tool với venv
alias snapshot='cd /mnt/d/ytb-downloader && source venv/bin/activate && python video_snapshot_tool.py'
```

Sau đó:
```bash
source ~/.bashrc
```

Bây giờ chỉ cần gõ `snapshot` để chạy tool.

## 10. QUICK START COMMANDS

Copy và paste các lệnh sau vào terminal:

```bash
# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài đặt Python và dependencies
sudo apt install python3 python3-pip python3-venv python3-tk python3-full -y

# 3. Cài đặt OpenCV dependencies
sudo apt install libopencv-dev python3-opencv ffmpeg -y

# 4. Di chuyển đến project
cd /mnt/d/ytb-downloader

# 5. Tạo virtual environment (BẮT BUỘC cho Python 3.12+)
python3 -m venv venv
source venv/bin/activate

# 6. Cài đặt thư viện (trong venv)
pip install -r requirements.txt

# 7. Thiết lập DISPLAY (nếu cần)
export DISPLAY=$(ip route list default | awk '{print $3}'):0.0

# 8. Chạy tool
python video_snapshot_tool.py
```

**Lưu ý**: Mỗi lần mở terminal mới, cần chạy lại:
```bash
cd /mnt/d/ytb-downloader
source venv/bin/activate
python video_snapshot_tool.py
```

## 11. LƯU Ý QUAN TRỌNG

1. **WSL1 vs WSL2**: WSL2 nhanh hơn và hỗ trợ tốt hơn, khuyến nghị dùng WSL2
2. **File system**: File trong `/mnt/c/` hoặc `/mnt/d/` sẽ chậm hơn so với file trong Linux filesystem
3. **GUI**: Cần X server để chạy GUI applications trong WSL
4. **Performance**: Copy file vào Linux filesystem (`~/`) để tăng tốc độ xử lý

## 12. TỐI ƯU HIỆU NĂNG

### Copy video vào Linux filesystem trước khi xử lý:

```bash
# Tạo thư mục
mkdir -p ~/videos

# Copy video từ Windows
cp /mnt/d/path/to/video.mp4 ~/videos/

# Xử lý từ Linux filesystem (nhanh hơn)
```

Chúc bạn cài đặt thành công! 🚀
