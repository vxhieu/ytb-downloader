# Video Snapshot Tool

Tool trích xuất snapshot từ video theo khoảng thời gian định sẵn.

## Tính năng

- ✅ Chọn video đầu vào (hỗ trợ MP4, AVI, MKV, MOV, WMV, FLV)
- ✅ Lựa chọn khoảng thời gian snapshot: 3s, 6s, 9s, 12s hoặc tùy chỉnh
- ✅ Chọn thư mục lưu snapshot
- ✅ Hiển thị thông tin video (độ dài, FPS, resolution)
- ✅ Progress bar và thống kê real-time
- ✅ Preview snapshot trong quá trình xử lý
- ✅ Điều khiển quá trình (Bắt đầu, Dừng, Xóa)
- ✅ Tự động tạo log file với danh sách snapshot

## Cài đặt

### Yêu cầu
- Python 3.8 trở lên

### Cài đặt trên Windows
Xem [Hướng dẫn cài đặt Windows](HUONG_DAN_SU_DUNG.md#cài-đặt)

### Cài đặt trên WSL (Windows Subsystem for Linux)
- ⚡ **Quick Start**: [QUICK_START_WSL.md](QUICK_START_WSL.md) - Giải quyết lỗi `externally-managed-environment`
- 📖 **Hướng dẫn chi tiết**: [HUONG_DAN_CAI_DAT_WSL.md](HUONG_DAN_CAI_DAT_WSL.md)

**⚠️ Lưu ý**: Với Python 3.12+ hoặc Ubuntu 23.04+, bạn **PHẢI** sử dụng virtual environment:

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### Cài đặt thư viện (Windows - không cần venv)

```bash
pip install -r requirements.txt
```

Hoặc cài đặt thủ công:
```bash
pip install opencv-python Pillow
```

## Sử dụng

Chạy ứng dụng:
```bash
python video_snapshot_tool.py
```

Hoặc nếu dùng venv (WSL):
```bash
source venv/bin/activate
python video_snapshot_tool.py
```

### Hướng dẫn nhanh

1. **Chọn video**: Click nút "Chọn Video" và chọn file video
2. **Chọn khoảng thời gian**: Chọn 3s, 6s, 9s, 12s hoặc nhập giá trị tùy chỉnh
3. **Chọn thư mục lưu**: Click nút "Chọn thư mục" và chọn nơi lưu snapshot
4. **Bắt đầu**: Click nút "Bắt đầu" để bắt đầu trích xuất
5. **Theo dõi**: Xem progress bar và preview trong quá trình xử lý

## Tài liệu

- [Phân tích hệ thống](PHAN_TICH_HE_THONG.md) - Kiến trúc và thiết kế hệ thống
- [Hướng dẫn sử dụng](HUONG_DAN_SU_DUNG.md) - Hướng dẫn chi tiết cách sử dụng
- [Quick Start WSL](QUICK_START_WSL.md) - ⚡ Giải quyết lỗi externally-managed-environment
- [Hướng dẫn cài đặt WSL](HUONG_DAN_CAI_DAT_WSL.md) - Cài đặt Python và tool trên WSL
- [Danh sách chức năng](DANH_SACH_CHUC_NANG.md) - Tổng hợp tất cả tính năng

## Scripts hỗ trợ

- `setup_venv.sh` - Tự động tạo và thiết lập virtual environment
- `install_wsl.sh` - Script cài đặt đầy đủ cho WSL
- `fix_venv.sh` - Sửa lỗi python3-venv

## Format file output

Snapshot được lưu với format:
```
snapshot_MMMSS_XXXX.png
```

Trong đó:
- `MMMSS`: Phút và giây trong video (ví dụ: 00123 = 1 phút 23 giây)
- `XXXX`: Số thứ tự snapshot (0001, 0002, 0003...)

File log `extraction_log.txt` được tạo tự động trong thư mục output, chứa:
- Thông tin video và cài đặt
- Danh sách tất cả snapshot đã tạo
- Timestamp của mỗi snapshot

## Lưu ý

- Snapshot giữ nguyên độ phân giải gốc của video
- Format PNG đảm bảo chất lượng tốt nhất
- Đảm bảo có đủ dung lượng trống cho output
- Xử lý video lớn có thể mất nhiều thời gian
- Với WSL, khuyến nghị dùng virtual environment

## Phát triển

### Cấu trúc code
- `video_snapshot_tool.py`: File chính chứa GUI và logic xử lý
- `requirements.txt`: Danh sách thư viện cần thiết

### Tính năng sắp tới
- Batch processing (xử lý nhiều video)
- Tùy chỉnh chất lượng ảnh (JPEG quality)
- Frame selection mode (chọn frame cụ thể)
- Resume functionality
- Thumbnail grid view

## License

MIT License - Tự do sử dụng và chỉnh sửa

## Tác giả

Video Snapshot Tool - 2024
