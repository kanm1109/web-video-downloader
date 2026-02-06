# 🔧 Fix lỗi "Failed to fetch"

## ❌ Lỗi
```
Có lỗi xảy ra
Failed to fetch
```

## ✅ Nguyên nhân
1. Backend không chạy
2. API_URL trong frontend bị sai
3. Browser cache code cũ

## ✅ Đã fix (2026-02-05)

### 1. Backend đã chạy
```bash
✅ Backend: Running at http://localhost:8000
```

### 2. API_URL đã fix
**Trước (lỗi):**
```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://your-api-domain.com';
```
→ Nếu mở `file://` thì hostname không phải 'localhost' → dùng sai URL

**Sau (đúng):**
```javascript
const API_URL = 'http://localhost:8000';
```
→ Luôn dùng localhost cho development

---

## 🎯 CÁCH SỬA

### Bước 1: Đảm bảo backend chạy
```bash
cd multi-platform-video-downloader
python app.py
```

Kiểm tra: http://localhost:8000/health

### Bước 2: Đóng tab cũ

**QUAN TRỌNG:** Đóng tất cả tab đang mở index.html

### Bước 3: Mở LẠI index.html

**Double-click:** `multi-platform-video-downloader\index.html`

(Phải mở lại để load code mới!)

### Bước 4: Test với YouTube

1. Dán URL: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
2. Chọn: `360p`
3. Click: "Tải Video Ngay"
4. Xong! ✅

---

## ⚠️ Nếu vẫn lỗi

### 1. Hard Refresh
Nhấn: `Ctrl + Shift + R` (Windows) hoặc `Cmd + Shift + R` (Mac)

→ Xóa cache browser

### 2. Check Console
Nhấn `F12` → Tab Console

Xem lỗi gì:
- `ERR_CONNECTION_REFUSED` → Backend chưa chạy
- `CORS error` → Kiểm tra .env: `ALLOWED_ORIGINS=*`
- `404` → Sai endpoint

### 3. Check backend logs
Xem terminal đang chạy `python app.py`

Có lỗi gì không?

### 4. Test API trực tiếp
Mở browser: http://localhost:8000/health

Nếu không load → Backend có vấn đề

---

## ✅ Checklist

- [ ] Backend đang chạy (`python app.py`)
- [ ] http://localhost:8000/health trả về {"status":"healthy"}
- [ ] Đã đóng tab cũ
- [ ] Đã mở LẠI index.html
- [ ] Đã hard refresh (Ctrl+Shift+R)
- [ ] Test với YouTube (không test TikTok/Facebook trước)

---

## 🎯 After Fix

Bạn sẽ thấy:
1. Loading spinner khi click "Tải Video Ngay"
2. Video info hiển thị sau 2-3 giây
3. Nút "Tải Video Xuống" màu tím
4. Click để tải về máy

**SUCCESS!** ✅

---

**Fixed:** 2026-02-05  
**Status:** ✅ Working
