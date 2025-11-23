# QUICK START - WSL (Giải quyết lỗi externally-managed-environment)

## ⚡ Giải pháp nhanh

Nếu bạn gặp lỗi `externally-managed-environment`, làm theo các bước sau:

### Bước 1: Di chuyển đến thư mục project
```bash
cd /mnt/d/ytb-downloader
```

### Bước 2: Tạo virtual environment
```bash
python3 -m venv venv
```

### Bước 3: Kích hoạt virtual environment
```bash
source venv/bin/activate
```

Bạn sẽ thấy `(venv)` ở đầu dòng prompt.

### Bước 4: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 5: Chạy tool
```bash
python video_snapshot_tool.py
```

## 📝 Lưu ý quan trọng

**Mỗi lần mở terminal mới**, bạn cần:
1. `cd /mnt/d/ytb-downloader`
2. `source venv/bin/activate`
3. `python video_snapshot_tool.py`

## 🚀 Tạo alias để tiện hơn

Thêm vào `~/.bashrc`:
```bash
alias snapshot='cd /mnt/d/ytb-downloader && source venv/bin/activate && python video_snapshot_tool.py'
```

Sau đó:
```bash
source ~/.bashrc
```

Bây giờ chỉ cần gõ `snapshot` để chạy tool!

## 🔧 Sử dụng script tự động

Chạy script setup:
```bash
bash setup_venv.sh
```

Hoặc script cài đặt đầy đủ:
```bash
bash install_wsl.sh
```

## ❓ Tại sao cần virtual environment?

- Python 3.12+ và Ubuntu 23.04+ có tính năng bảo vệ system packages
- Virtual environment tách biệt packages của project với system
- Tránh conflict và giữ system Python sạch sẽ
- Đây là best practice trong Python development

## 🆘 Vẫn gặp lỗi?

Xem hướng dẫn chi tiết: [HUONG_DAN_CAI_DAT_WSL.md](HUONG_DAN_CAI_DAT_WSL.md)
