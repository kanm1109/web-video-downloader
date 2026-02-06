# ⚡ Quick Start - Chạy trong 5 phút

## Cách nhanh nhất để test project

### Bước 1: Cài đặt

```bash
cd multi-platform-video-downloader
pip install -r requirements.txt
```

### Bước 2: Chạy Backend

```bash
python app.py
```

Server chạy tại: http://localhost:8000

### Bước 3: Mở Frontend

**Option 1 - Python:**
```bash
python -m http.server 3000
```

**Option 2 - Mở trực tiếp file:**
- Double click `index.html`
- Hoặc kéo thả vào Chrome/Firefox

**Option 3 - VS Code:**
- Cài extension "Live Server"
- Right click `index.html` → Open with Live Server

### Bước 4: Test

1. Mở: http://localhost:3000 (hoặc file:// nếu mở trực tiếp)
2. Dán link TikTok: `https://www.tiktok.com/@user/video/123`
3. Click "Tải Video Ngay"
4. Xong! 🎉

---

## ❗ Nếu gặp lỗi CORS

Cập nhật `index.html`, dòng:

```javascript
const API_URL = 'http://localhost:8000';
```

Và trong `.env`:

```env
ALLOWED_ORIGINS=*
```

Restart backend.

---

## 🧪 Test với cURL

```bash
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.tiktok.com/@user/video/123","quality":"best"}'
```

Done! ✅
