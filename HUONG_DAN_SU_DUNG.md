# HƯỚNG DẪN SỬ DỤNG - VIDEO SNAPSHOT TOOL

## 1. CÀI ĐẶT

### 1.1. Yêu cầu hệ thống
- Windows 10/11, macOS, hoặc Linux
- Python 3.8 trở lên
- Kết nối internet để cài đặt thư viện (lần đầu)

### 1.2. Cài đặt Python và thư viện

#### Bước 1: Kiểm tra Python
Mở Command Prompt/Terminal và chạy:
```bash
python --version
```
Hoặc:
```bash
python3 --version
```

#### Bước 2: Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

Hoặc nếu dùng Python 3:
```bash
pip3 install -r requirements.txt
```

### 1.3. Chạy ứng dụng
```bash
python video_snapshot_tool.py
```

## 2. HƯỚNG DẪN SỬ DỤNG

### 2.1. Giao diện chính

```
┌─────────────────────────────────────────────┐
│     VIDEO SNAPSHOT TOOL                     │
├─────────────────────────────────────────────┤
│                                             │
│  [Chọn Video]  [video_file.mp4]            │
│                                             │
│  Khoảng thời gian snapshot:                 │
│  ○ 3 giây (khuyến nghị)                    │
│  ○ 6 giây                                    │
│  ○ 9 giây                                    │
│  ○ 12 giây                                   │
│  ○ Tùy chỉnh: [____] giây                   │
│                                             │
│  [Chọn thư mục lưu]  [C:\Snapshots\]       │
│                                             │
│  Thông tin video:                           │
│  - Độ dài: 00:05:30                         │
│  - FPS: 30                                  │
│  - Resolution: 1920x1080                    │
│  - Số snapshot dự kiến: 110                 │
│                                             │
│  [Bắt đầu]  [Dừng]  [Xóa]                   │
│                                             │
│  Tiến trình: [████████░░] 80%               │
│  Đã tạo: 88/110 snapshots                   │
│                                             │
│  Preview:                                   │
│  [Ảnh snapshot mẫu]                        │
│                                             │
└─────────────────────────────────────────────┘
```

### 2.2. Các bước sử dụng

#### Bước 1: Chọn video
1. Click nút **"Chọn Video"** hoặc **"Browse Video"**
2. Trong hộp thoại, chọn file video cần xử lý
3. Hệ thống sẽ tự động load thông tin video (độ dài, FPS, resolution)

#### Bước 2: Chọn khoảng thời gian snapshot
- **3 giây** (khuyến nghị): Phù hợp cho hầu hết trường hợp
- **6 giây**: Ít snapshot hơn, phù hợp video dài
- **9 giây**: Rất ít snapshot, phù hợp video rất dài
- **12 giây**: Cực kỳ ít snapshot
- **Tùy chỉnh**: Nhập số giây bất kỳ (ví dụ: 5, 7.5, 15)

**Lưu ý**: 
- Giá trị phải lớn hơn 0
- Giá trị quá nhỏ (< 0.5s) có thể tạo quá nhiều ảnh
- Giá trị quá lớn có thể bỏ lỡ các khoảnh khắc quan trọng

#### Bước 3: Chọn thư mục lưu
1. Click nút **"Chọn thư mục lưu"** hoặc **"Browse Folder"**
2. Chọn thư mục muốn lưu các snapshot
3. Hoặc tạo thư mục mới trong hộp thoại

**Lưu ý**: 
- Đảm bảo có đủ dung lượng trống
- Tên file snapshot sẽ có format: `snapshot_MMMSS_XXX.png`

#### Bước 4: Xem thông tin và bắt đầu
1. Kiểm tra thông tin video hiển thị
2. Xem số lượng snapshot dự kiến
3. Click nút **"Bắt đầu"** hoặc **"Start Extraction"**

#### Bước 5: Theo dõi tiến trình
- Thanh progress bar hiển thị phần trăm hoàn thành
- Số lượng snapshot đã tạo / tổng số
- Preview snapshot mới nhất (nếu bật)
- Có thể click **"Dừng"** để tạm dừng

#### Bước 6: Hoàn thành
- Khi hoàn thành, sẽ có thông báo
- Hiển thị tổng số snapshot đã tạo
- Có thể mở thư mục output để xem kết quả
- File log `extraction_log.txt` được tạo tự động

## 3. VÍ DỤ SỬ DỤNG

### Ví dụ 1: Tạo snapshot mỗi 3 giây từ video 5 phút
- **Input**: `my_video.mp4` (5 phút = 300 giây)
- **Interval**: 3 giây
- **Output**: ~100 snapshot (300 / 3)
- **Thời gian xử lý**: ~2-5 phút (tùy độ phân giải)

### Ví dụ 2: Tạo snapshot mỗi 6 giây từ video 1 giờ
- **Input**: `long_video.mp4` (1 giờ = 3600 giây)
- **Interval**: 6 giây
- **Output**: ~600 snapshot (3600 / 6)
- **Thời gian xử lý**: ~10-20 phút

### Ví dụ 3: Tùy chỉnh interval 7.5 giây
- **Input**: `custom_video.mp4`
- **Interval**: 7.5 giây (custom)
- **Output**: Tùy theo độ dài video

## 4. TÍNH NĂNG NÂNG CAO

### 4.1. Preview snapshot
- Bật preview để xem snapshot trước khi lưu
- Tự động cập nhật mỗi 3 snapshot

### 4.2. Export log
- Tự động tạo file `extraction_log.txt` trong output folder
- Chứa danh sách tất cả snapshot đã tạo với timestamp
- Format: CSV-like với thông tin chi tiết

## 5. XỬ LÝ SỰ CỐ

### 5.1. Lỗi "Cannot read video file"
- **Nguyên nhân**: File video bị hỏng hoặc format không hỗ trợ
- **Giải pháp**: 
  - Kiểm tra file video có mở được bằng player khác không
  - Thử convert video sang MP4 format
  - Kiểm tra đường dẫn file có đúng không

### 5.2. Lỗi "Insufficient disk space"
- **Nguyên nhân**: Không đủ dung lượng để lưu snapshot
- **Giải pháp**:
  - Chọn thư mục khác có nhiều dung lượng hơn
  - Tăng interval để giảm số lượng snapshot
  - Xóa file không cần thiết

### 5.3. Lỗi "Invalid interval value"
- **Nguyên nhân**: Giá trị interval không hợp lệ
- **Giải pháp**:
  - Nhập số dương (ví dụ: 1, 2.5, 10)
  - Không được nhập số âm hoặc 0
  - Không được nhập chữ

### 5.4. Ứng dụng chạy chậm
- **Nguyên nhân**: Video quá lớn hoặc độ phân giải cao
- **Giải pháp**:
  - Tăng interval để giảm số snapshot
  - Đóng các ứng dụng khác để giải phóng RAM
  - Giảm độ phân giải video trước khi xử lý (tính năng tương lai)

## 6. MẸO VÀ THỦ THUẬT

### 6.1. Tối ưu số lượng snapshot
- Video ngắn (< 1 phút): Dùng interval 1-2 giây
- Video trung bình (1-10 phút): Dùng interval 3-6 giây
- Video dài (> 10 phút): Dùng interval 6-12 giây

### 6.2. Chất lượng ảnh
- Snapshot giữ nguyên độ phân giải gốc của video
- Format PNG giữ chất lượng tốt nhất (file lớn hơn)
- Format JPEG nhỏ hơn nhưng có thể mất chất lượng (tính năng tương lai)

### 6.3. Đặt tên file
- Format: `snapshot_MMMSS_XXX.png`
- `MMMSS`: Phút và giây trong video (ví dụ: 00123 = 1 phút 23 giây)
- `XXX`: Số thứ tự snapshot (0001, 0002, 0003...)

## 7. FAQ (Câu hỏi thường gặp)

**Q: Tool có hỗ trợ video 4K không?**
A: Có, nhưng xử lý sẽ chậm hơn và file snapshot sẽ lớn hơn.

**Q: Có thể tạm dừng và tiếp tục không?**
A: Hiện tại chưa hỗ trợ resume, nhưng có thể dừng và bắt đầu lại.

**Q: Snapshot có giữ nguyên chất lượng video không?**
A: Có, snapshot giữ nguyên độ phân giải và chất lượng frame gốc.

**Q: Có thể chọn frame cụ thể không?**
A: Tính năng này đang được phát triển, hiện tại chỉ hỗ trợ interval tự động.

**Q: Tool có miễn phí không?**
A: Có, tool hoàn toàn miễn phí và mã nguồn mở.
