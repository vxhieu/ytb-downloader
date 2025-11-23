# DANH SÁCH CHỨC NĂNG - VIDEO SNAPSHOT TOOL

## 1. CHỨC NĂNG CỐT LÕI (CORE FEATURES)

### ✅ 1.1. Chọn Video Đầu Vào
- **Mô tả**: Cho phép người dùng chọn file video từ hệ thống
- **Chi tiết**:
  - File browser dialog
  - Hỗ trợ nhiều format: MP4, AVI, MKV, MOV, WMV, FLV
  - Validation file format
  - Hiển thị đường dẫn file đã chọn
  - Drag & drop support (tính năng nâng cao)

### ✅ 1.2. Thiết Lập Khoảng Thời Gian Snapshot
- **Mô tả**: Cho phép người dùng chọn khoảng thời gian giữa các snapshot
- **Chi tiết**:
  - **Option 3 giây** (khuyến nghị): Mặc định, phù hợp hầu hết trường hợp
  - **Option 6 giây**: Ít snapshot hơn, phù hợp video dài
  - **Option 9 giây**: Rất ít snapshot
  - **Option 12 giây**: Cực kỳ ít snapshot
  - **Option Custom**: Nhập giá trị tùy chỉnh (số thập phân được hỗ trợ)
  - Validation input (phải > 0)
  - Real-time tính toán số snapshot dự kiến

### ✅ 1.3. Chọn Thư Mục Lưu Trữ
- **Mô tả**: Cho phép người dùng chọn nơi lưu các snapshot
- **Chi tiết**:
  - Folder browser dialog
  - Tạo thư mục mới nếu chưa tồn tại
  - Hiển thị đường dẫn thư mục đã chọn
  - Kiểm tra quyền ghi file
  - Kiểm tra dung lượng trống (cảnh báo nếu không đủ)

### ✅ 1.4. Trích Xuất Snapshot
- **Mô tả**: Xử lý video và tạo các snapshot theo interval đã chọn
- **Chi tiết**:
  - Đọc video file
  - Tính toán frame index dựa trên interval và FPS
  - Trích xuất frame tại các thời điểm cụ thể
  - Lưu ảnh với tên file có timestamp
  - Format tên file: `snapshot_MMMSS_XXX.png`
  - Hỗ trợ format PNG (chất lượng cao)

### ✅ 1.5. Hiển Thị Tiến Trình
- **Mô tả**: Hiển thị tiến độ xử lý cho người dùng
- **Chi tiết**:
  - Progress bar với phần trăm hoàn thành
  - Hiển thị số snapshot đã tạo / tổng số
  - Hiển thị thời gian còn lại (ước tính)
  - Update real-time trong quá trình xử lý

## 2. CHỨC NĂNG HỖ TRỢ (SUPPORT FEATURES)

### ✅ 2.1. Hiển Thị Thông Tin Video
- **Mô tả**: Hiển thị thông tin chi tiết về video đã chọn
- **Chi tiết**:
  - Độ dài video (giờ:phút:giây)
  - Frame rate (FPS)
  - Resolution (width x height)
  - Tổng số frame
  - Số snapshot dự kiến dựa trên interval
  - Dung lượng file video

### ✅ 2.2. Preview Snapshot
- **Mô tả**: Hiển thị snapshot mẫu trong quá trình xử lý
- **Chi tiết**:
  - Preview panel trong giao diện
  - Hiển thị snapshot mới nhất đã tạo
  - Tự động resize để fit trong preview area
  - Cập nhật mỗi 3 snapshot

### ✅ 2.3. Điều Khiển Quá Trình
- **Mô tả**: Các nút điều khiển quá trình xử lý
- **Chi tiết**:
  - **Nút "Bắt đầu"**: Bắt đầu quá trình trích xuất
  - **Nút "Dừng"**: Tạm dừng quá trình (có thể tiếp tục)
  - **Nút "Xóa/Hủy"**: Xóa lựa chọn và reset về trạng thái ban đầu
  - **Nút "Mở thư mục"**: Mở thư mục output trong file explorer

### ✅ 2.4. Validation và Error Handling
- **Mô tả**: Kiểm tra và xử lý lỗi
- **Chi tiết**:
  - Validate video file format
  - Validate interval value
  - Kiểm tra quyền ghi file
  - Kiểm tra dung lượng đĩa
  - Hiển thị error messages rõ ràng
  - Log errors vào file (tùy chọn)

### ✅ 2.5. Export Log File
- **Mô tả**: Tạo file log chứa thông tin extraction
- **Chi tiết**:
  - Tự động tạo `extraction_log.txt` trong output folder
  - Danh sách tất cả snapshot đã tạo
  - Timestamp của mỗi snapshot trong video
  - Đường dẫn file đầy đủ
  - Format: Text với thông tin chi tiết

## 3. CHỨC NĂNG NÂNG CAO (ADVANCED FEATURES)

### 🔄 3.1. Batch Processing
- **Mô tả**: Xử lý nhiều video cùng lúc
- **Chi tiết**:
  - Chọn nhiều video file
  - Queue system để xử lý tuần tự
  - Progress tracking cho từng video
  - Tổng hợp kết quả cuối cùng

### 🔄 3.2. Image Quality Settings
- **Mô tả**: Tùy chỉnh chất lượng ảnh output
- **Chi tiết**:
  - Format selection (PNG, JPEG)
  - JPEG quality slider (1-100)
  - Compression level cho PNG
  - Resolution scaling (giữ nguyên, 50%, 75%, custom)

### 🔄 3.3. Frame Selection Mode
- **Mô tả**: Chọn frame cụ thể thay vì interval tự động
- **Chi tiết**:
  - Timeline scrubber để chọn frame
  - Nhập timestamp cụ thể (MM:SS)
  - Chọn nhiều frame riêng lẻ
  - Preview frame trước khi lưu

### 🔄 3.4. Thumbnail Grid View
- **Mô tả**: Hiển thị tất cả snapshot dưới dạng grid
- **Chi tiết**:
  - Grid layout với thumbnails
  - Click để xem full size
  - Filter và search snapshots
  - Export grid thành một ảnh lớn

### 🔄 3.5. Resume/Pause Functionality
- **Mô tả**: Tạm dừng và tiếp tục quá trình xử lý
- **Chi tiết**:
  - Lưu progress vào file
  - Resume từ điểm dừng
  - Skip các snapshot đã tạo
  - Recovery sau khi crash

### 🔄 3.6. Video Info Export
- **Mô tả**: Export thông tin video ra file
- **Chi tiết**:
  - Export metadata (JSON/XML)
  - Frame analysis (keyframes, scene changes)
  - Statistics về video

### 🔄 3.7. Custom Naming Pattern
- **Mô tả**: Tùy chỉnh pattern đặt tên file
- **Chi tiết**:
  - Template system
  - Variables: {timestamp}, {index}, {video_name}
  - Preview tên file trước khi lưu

## 4. CHỨC NĂNG GIAO DIỆN (UI FEATURES)

### ✅ 4.1. Modern GUI Design
- **Mô tả**: Giao diện hiện đại, dễ sử dụng
- **Chi tiết**:
  - Clean và intuitive layout
  - Responsive design
  - Dark/Light theme (tính năng nâng cao)
  - Tooltips cho các controls
  - Keyboard shortcuts

### ✅ 4.2. Real-time Updates
- **Mô tả**: Cập nhật thông tin real-time
- **Chi tiết**:
  - Progress bar update
  - Counter update
  - Preview refresh
  - Status messages

### ✅ 4.3. User Feedback
- **Mô tả**: Phản hồi rõ ràng cho người dùng
- **Chi tiết**:
  - Success notifications
  - Error messages
  - Warning dialogs
  - Confirmation dialogs

## 5. CHỨC NĂNG KỸ THUẬT (TECHNICAL FEATURES)

### ✅ 5.1. Multi-threading
- **Mô tả**: Xử lý không block UI
- **Chi tiết**:
  - Background processing thread
  - UI thread riêng biệt
  - Thread-safe operations

### ✅ 5.2. Memory Management
- **Mô tả**: Quản lý bộ nhớ hiệu quả
- **Chi tiết**:
  - Không load toàn bộ video vào RAM
  - Frame-by-frame processing
  - Garbage collection
  - Memory usage monitoring

### ✅ 5.3. Performance Optimization
- **Mô tả**: Tối ưu hiệu năng
- **Chi tiết**:
  - Frame seeking thay vì đọc tuần tự
  - Batch file operations
  - Efficient image encoding
  - Progress caching

## 6. ROADMAP - TÍNH NĂNG TƯƠNG LAI

### 📅 Phase 1 (Hiện tại)
- ✅ Core features
- ✅ Basic UI
- ✅ Progress tracking
- ✅ Preview
- ✅ Log export

### 📅 Phase 2 (Sắp tới)
- 🔄 Batch processing
- 🔄 Image quality settings
- 🔄 Resume functionality

### 📅 Phase 3 (Tương lai)
- 🔄 Frame selection mode
- 🔄 Thumbnail grid view
- 🔄 Custom naming patterns
- 🔄 Video analysis features
- 🔄 Web interface
- 🔄 API support

## 7. TỔNG KẾT

### Chức năng đã triển khai: 15/25
### Chức năng đang phát triển: 7/25
### Chức năng trong roadmap: 3/25

**Ưu tiên phát triển tiếp theo:**
1. Batch processing
2. Image quality settings
3. Resume functionality
4. Frame selection mode
5. Thumbnail grid view
