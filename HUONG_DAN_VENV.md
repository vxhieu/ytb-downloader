# HƯỚNG DẪN VỀ VIRTUAL ENVIRONMENT (VENV)

## 🔍 VIRTUAL ENVIRONMENT LÀ GÌ?

Virtual Environment (venv) là một môi trường Python độc lập, tách biệt với system Python. Nó cho phép:
- Cài đặt packages riêng cho từng project
- Tránh conflict giữa các project
- Giữ system Python sạch sẽ
- **BẮT BUỘC** với Python 3.12+ để tránh lỗi "externally-managed-environment"

## 🎯 TẠI SAO CẦN KÍCH HOẠT VENV?

Khi bạn kích hoạt venv:
- Lệnh `python` sẽ trỏ đến Python trong venv (không phải system Python)
- Lệnh `pip` sẽ cài đặt packages vào venv (không phải system)
- Bạn có thể cài đặt packages mà không gặp lỗi "externally-managed-environment"

## 📝 CÁCH KÍCH HOẠT VENV

### Trên WSL/Linux:

```bash
# Di chuyển đến thư mục project
cd /mnt/d/ytb-downloader

# Kích hoạt venv
source venv/bin/activate
```

**Sau khi kích hoạt, bạn sẽ thấy `(venv)` ở đầu dòng prompt:**
```
(venv) user@computer:/mnt/d/ytb-downloader$
```

### Trên Windows (PowerShell):

```powershell
cd D:\ytb-downloader
venv\Scripts\Activate.ps1
```

### Trên Windows (Command Prompt):

```cmd
cd D:\ytb-downloader
venv\Scripts\activate.bat
```

## ✅ KIỂM TRA ĐÃ KÍCH HOẠT CHƯA

Sau khi chạy `source venv/bin/activate`, kiểm tra:

```bash
# Kiểm tra biến môi trường
echo $VIRTUAL_ENV

# Hoặc kiểm tra đường dẫn Python
which python
# Sẽ hiển thị: /mnt/d/ytb-downloader/venv/bin/python
```

## 🚀 SAU KHI KÍCH HOẠT, BẠN CÓ THỂ:

### 1. Cài đặt packages (KHÔNG CÒN LỖI!)
```bash
pip install -r requirements.txt
```

### 2. Chạy tool
```bash
python video_snapshot_tool.py
```

### 3. Kiểm tra packages đã cài
```bash
pip list
```

## 🔄 THOÁT KHỎI VENV

Khi xong việc, bạn có thể thoát:

```bash
deactivate
```

Sau đó prompt sẽ trở lại bình thường (không còn `(venv)`).

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Mỗi lần mở terminal mới**, bạn PHẢI kích hoạt lại venv
2. **Luôn kích hoạt venv trước khi**:
   - Cài đặt packages (`pip install`)
   - Chạy tool (`python video_snapshot_tool.py`)
3. **Nếu quên kích hoạt**, bạn sẽ gặp lỗi "externally-managed-environment"

## 🎯 VÍ DỤ ĐẦY ĐỦ

```bash
# Bước 1: Di chuyển đến project
cd /mnt/d/ytb-downloader

# Bước 2: Kích hoạt venv
source venv/bin/activate

# Bước 3: Kiểm tra (sẽ thấy (venv) ở đầu dòng)
# (venv) user@computer:/mnt/d/ytb-downloader$

# Bước 4: Cài đặt packages (nếu chưa cài)
pip install -r requirements.txt

# Bước 5: Chạy tool
python video_snapshot_tool.py

# Bước 6: Khi xong, thoát venv (tùy chọn)
deactivate
```

## 🚀 TẠO ALIAS ĐỂ TIỆN HƠN

Thay vì phải nhớ kích hoạt mỗi lần, tạo alias:

```bash
# Thêm vào ~/.bashrc
alias snapshot='cd /mnt/d/ytb-downloader && source venv/bin/activate && python video_snapshot_tool.py'

# Load lại
source ~/.bashrc
```

Bây giờ chỉ cần gõ `snapshot` để chạy tool!

## ❓ CÂU HỎI THƯỜNG GẶP

**Q: Tại sao phải kích hoạt venv mỗi lần?**
A: Vì mỗi terminal session là độc lập. Khi đóng terminal, venv sẽ tự động deactivate.

**Q: Có thể chạy tool mà không cần kích hoạt venv không?**
A: Có! Bạn có thể chạy trực tiếp:
```bash
venv/bin/python video_snapshot_tool.py
```

**Q: Làm sao biết đang dùng venv hay system Python?**
A: Kiểm tra đường dẫn:
```bash
which python
# Nếu là venv: /mnt/d/ytb-downloader/venv/bin/python
# Nếu là system: /usr/bin/python3
```

**Q: Venv có tốn nhiều dung lượng không?**
A: Không nhiều, thường khoảng 50-100MB. Mỗi project có venv riêng là best practice.




