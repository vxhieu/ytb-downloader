# HƯỚNG DẪN CÀI ĐẶT NHANH - Giải quyết lỗi externally-managed-environment

## ⚠️ LỖI: externally-managed-environment

Lỗi này xảy ra khi bạn cố gắng cài đặt packages trực tiếp vào system Python. **BẮT BUỘC** phải dùng virtual environment!

## ✅ GIẢI PHÁP NHANH (3 bước)

### Bước 1: Kích hoạt virtual environment

```bash
cd /mnt/d/ytb-downloader
source venv/bin/activate
```

Bạn sẽ thấy `(venv)` ở đầu dòng prompt.

### Bước 2: Cài đặt packages (trong venv)

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy tool

```bash
python video_snapshot_tool.py
```

## 🔧 NẾU VENV CHƯA TỒN TẠI HOẶC BỊ LỖI

### Cách 1: Sử dụng script tự động (KHUYẾN NGHỊ)

```bash
cd /mnt/d/ytb-downloader
bash setup_venv.sh
```

Script này sẽ:
- Tự động tạo venv nếu chưa có
- Cài đặt tất cả packages
- Kiểm tra cài đặt

### Cách 2: Tạo thủ công

```bash
cd /mnt/d/ytb-downloader

# Xóa venv cũ nếu có lỗi
rm -rf venv

# Tạo venv mới
python3 -m venv venv

# Kích hoạt
source venv/bin/activate

# Cài đặt packages
pip install -r requirements.txt

# Chạy tool
python video_snapshot_tool.py
```

## 📝 LƯU Ý QUAN TRỌNG

**Mỗi lần mở terminal mới**, bạn PHẢI kích hoạt venv:

```bash
cd /mnt/d/ytb-downloader
source venv/bin/activate
python video_snapshot_tool.py
```

## 🚀 TẠO ALIAS ĐỂ TIỆN HƠN

Thêm vào `~/.bashrc`:

```bash
alias snapshot='cd /mnt/d/ytb-downloader && source venv/bin/activate && python video_snapshot_tool.py'
```

Sau đó:
```bash
source ~/.bashrc
```

Bây giờ chỉ cần gõ `snapshot` để chạy tool!

## ❓ TẠI SAO CẦN VENV?

- Python 3.12+ và Ubuntu 23.04+ bảo vệ system packages
- Venv tách biệt packages của project với system
- Tránh conflict và giữ system Python sạch sẽ
- Đây là best practice trong Python development

## 🆘 VẪN GẶP LỖI?

1. Kiểm tra python3-venv đã cài chưa:
   ```bash
   sudo apt install python3-venv python3-full -y
   ```

2. Chạy script fix:
   ```bash
   bash fix_venv.sh
   ```

3. Xem hướng dẫn chi tiết: [HUONG_DAN_CAI_DAT_WSL.md](HUONG_DAN_CAI_DAT_WSL.md)




