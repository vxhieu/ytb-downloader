# 🎬 Video Snapshot Tool

Tool trích xuất snapshot từ video theo khoảng thời gian định sẵn với giao diện đẹp và dễ sử dụng.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20WSL%20%7C%20Linux-lightgrey.svg)

## ✨ Tính năng

- ✅ **Giao diện đẹp và hiện đại** - UI được thiết kế với màu sắc và typography chuyên nghiệp
- ✅ **Hỗ trợ nhiều format video** - MP4, AVI, MKV, MOV, WMV, FLV
- ✅ **Lựa chọn khoảng thời gian linh hoạt** - 3s, 6s, 9s, 12s hoặc tùy chỉnh
- ✅ **Preview real-time** - Xem snapshot trong quá trình xử lý với khả năng scroll
- ✅ **Progress bar và thống kê** - Theo dõi tiến trình chi tiết
- ✅ **Lưu đường dẫn mặc định** - Tự động nhớ thư mục đã chọn (config.json)
- ✅ **Hỗ trợ WSL và Windows Native** - Chạy trên cả Windows và WSL
- ✅ **Tự động cài đặt** - Script launcher tự động kiểm tra và cài đặt dependencies

## 🚀 Cài đặt nhanh

### Windows (Khuyến nghị - Chỉ cần double-click!)

1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/video-snapshot-tool.git
   cd video-snapshot-tool
   ```

2. **Double-click `start.bat`** - Script sẽ tự động:
   - Phát hiện môi trường (Windows Native hoặc WSL)
   - Kiểm tra và cài đặt dependencies
   - Chạy ứng dụng ngay lập tức

### WSL / Linux

```bash
# Clone repository
git clone https://github.com/yourusername/video-snapshot-tool.git
cd video-snapshot-tool

# Cài đặt
chmod +x install.sh
./install.sh

# Chạy ứng dụng
chmod +x run.sh
./run.sh
```

### Cài đặt thủ công

**Yêu cầu:**
- Python 3.8 trở lên
- pip

**Cài đặt:**
```bash
pip install -r requirements.txt
```

**Chạy:**
```bash
python video_snapshot_tool.py
```

## 📖 Hướng dẫn sử dụng

### Cách sử dụng cơ bản

1. **Chọn video**: Click nút "📂 Chọn Video" hoặc nhập đường dẫn trực tiếp
2. **Chọn khoảng thời gian**: Chọn 3s, 6s, 9s, 12s hoặc nhập giá trị tùy chỉnh
3. **Chọn thư mục lưu**: Click nút "📂 Chọn thư mục" hoặc nhập đường dẫn trực tiếp
4. **Bắt đầu**: Click nút "▶️ Bắt đầu" để bắt đầu trích xuất
5. **Theo dõi**: Xem progress bar và preview trong quá trình xử lý

### Cấu hình mặc định

File `config.json` tự động lưu đường dẫn mặc định. Để sử dụng:

1. Copy `config.json.example` thành `config.json`
2. Điền đường dẫn mặc định:
   ```json
   {
       "default_video_folder": "/path/to/videos",
       "default_output_folder": "/path/to/output"
   }
   ```

## 🛠️ Scripts hỗ trợ

| Script | Mô tả |
|--------|-------|
| `start.bat` | **Launcher chính** - Double-click để chạy (tự động phát hiện môi trường) |
| `install.bat` | Cài đặt cho Windows Native |
| `install_wsl.bat` | Cài đặt cho WSL |
| `install.sh` | Cài đặt cho Linux/WSL (bash) |
| `run.bat` | Chạy ứng dụng (Windows Native) |
| `run_wsl.bat` | Chạy ứng dụng (WSL) |
| `run.sh` | Chạy ứng dụng (Linux/WSL) |

## 📁 Cấu trúc dự án

```
video-snapshot-tool/
├── video_snapshot_tool.py    # File chính
├── requirements.txt           # Dependencies
├── config.json.example       # Template config
├── start.bat                 # Launcher chính (Windows)
├── install*.bat/sh           # Scripts cài đặt
├── run*.bat/sh               # Scripts chạy ứng dụng
└── README.md                 # Tài liệu này
```

## 🎯 Format file output

Snapshot được lưu với format:
```
snapshot_MMMSS_XXXX.png
```

Trong đó:
- `MMMSS`: Phút và giây trong video (ví dụ: 00123 = 1 phút 23 giây)
- `XXXX`: Số thứ tự snapshot (0001, 0002, 0003...)

File log `extraction_log.txt` được tạo tự động trong thư mục output.

## 🔧 Troubleshooting

### Lỗi "Python chưa được cài đặt"
- **Windows**: Cài Python từ https://www.python.org/
- **WSL/Linux**: `sudo apt install python3 python3-pip -y`

### Lỗi "externally-managed-environment" (WSL)
Script tự động tạo virtual environment. Nếu vẫn lỗi:
```bash
sudo apt install python3-venv -y
```

### Lỗi "wsl: command not found"
Cài WSL: `wsl --install` trong PowerShell (Admin)

### Ứng dụng không mở
- Kiểm tra Python: `python --version`
- Chạy lại script cài đặt
- Kiểm tra file `config.json` có tồn tại

## 📝 Lưu ý

- Snapshot giữ nguyên độ phân giải gốc của video
- Format PNG đảm bảo chất lượng tốt nhất
- Đảm bảo có đủ dung lượng trống cho output
- Xử lý video lớn có thể mất nhiều thời gian
- Với WSL, khuyến nghị dùng virtual environment

## 🚧 Tính năng sắp tới

- [ ] Batch processing (xử lý nhiều video)
- [ ] Tùy chỉnh chất lượng ảnh (JPEG quality)
- [ ] Frame selection mode (chọn frame cụ thể)
- [ ] Resume functionality
- [ ] Thumbnail grid view

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 👤 Tác giả

**HieuVX**

- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Cảm ơn

Cảm ơn bạn đã sử dụng Video Snapshot Tool! Nếu thấy hữu ích, hãy ⭐ star repository này nhé!
