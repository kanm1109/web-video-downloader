# 🔧 Troubleshooting Guide

## ⚠️ Lỗi phổ biến và cách khắc phục

### 1. "Failed to fetch" / Cannot connect

**Nguyên nhân:** Backend chưa chạy

**Giải pháp:**
```bash
# Windows
cd multi-platform-video-downloader
start_backend.bat

# Hoặc
python app.py
```

Kiểm tra: http://localhost:8000/health

---

### 2. TikTok: "Your IP address is blocked"

**Nguyên nhân:** TikTok chặn IP của bạn (phổ biến)

**Giải pháp:**

#### Option A: Dùng VPN
1. Bật VPN (ProtonVPN, NordVPN...)
2. Chọn server US/Europe
3. Thử lại

#### Option B: Dùng Proxy (Khuyến nghị cho production)
```python
# Thêm vào .env
PROXY_URL=http://proxy-server:port
```

Trong `app.py` thêm:
```python
if os.getenv('PROXY_URL'):
    ydl_opts['proxy'] = os.getenv('PROXY_URL')
```

#### Option C: Dùng cookies từ browser
1. Đăng nhập TikTok trên Chrome/Firefox
2. Export cookies (dùng extension "Get cookies.txt LOCALLY")
3. Lưu vào file `cookies.txt`
4. Update code:
```python
ydl_opts['cookiefile'] = 'cookies.txt'
```

#### Option D: Test với nền tảng khác
- YouTube (luôn hoạt động tốt)
- Instagram
- Facebook

---

### 3. "Rate limit exceeded"

**Nguyên nhân:** Quá 30 requests/phút

**Giải pháp:**
- Đợi 1 phút
- Hoặc tăng limit trong `.env`:
```env
MAX_REQUESTS_PER_MINUTE=60
```

---

### 4. YouTube: "Video unavailable"

**Nguyên nhân:** Video bị hạn chế khu vực hoặc private

**Giải pháp:**
- Test với video public khác
- Dùng VPN nếu video bị geo-restrict

---

### 5. Video không có thumbnail

**Nguyên nhân:** Bình thường, một số video không có

**Giải pháp:** Không cần fix, đã có placeholder image

---

### 6. Tốc độ chậm

**Giải pháp:**

#### Enable Redis cache:
```bash
# Install Redis
# Windows: Download từ https://github.com/microsoftarchive/redis/releases
# Linux: sudo apt install redis-server

# Update .env
REDIS_ENABLED=True
REDIS_HOST=localhost
```

#### Optimize yt-dlp:
```python
ydl_opts['socket_timeout'] = 10
ydl_opts['retries'] = 3
```

---

## 🧪 Test từng bước

### Step 1: Kiểm tra Backend
```bash
curl http://localhost:8000/health
```

Kết quả mong đợi:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "cache_size": 0
}
```

### Step 2: Test với YouTube (dễ nhất)
```bash
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=jNQXAC9IVRw","quality":"360p"}'
```

### Step 3: Test Frontend
Mở: http://localhost:3000
- Dán URL YouTube
- Chọn quality: 360p (nhanh nhất)
- Click download

---

## 🌍 TikTok IP Block - Giải thích

**Tại sao TikTok block IP?**

TikTok có rate limiting rất strict:
- Limit requests từ cùng 1 IP
- Phát hiện bot/scraper
- Geo-restriction

**Các dấu hiệu bị block:**
- "Your IP address is blocked"
- "Video unavailable" (trên video public)
- Timeout sau vài requests

**Giải pháp tốt nhất cho production:**

1. **Proxy Rotation** ($10-30/tháng)
   - Bright Data
   - Oxylabs
   - Smartproxy

2. **VPN Pool**
   - Nhiều VPN servers
   - Rotate giữa các requests

3. **Server ở nước khác**
   - US server thường work tốt hơn
   - EU servers cũng OK

---

## 💡 Tips để tránh bị block

### 1. Add delays
```python
import time
time.sleep(random.uniform(1, 3))  # Random delay
```

### 2. Rotate User-Agents
```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
    # ... more
]
ydl_opts['user_agent'] = random.choice(USER_AGENTS)
```

### 3. Respect rate limits
```python
MAX_REQUESTS_PER_MINUTE = 10  # Thấp hơn = an toàn hơn
```

### 4. Cache aggressively
```python
CACHE_TTL = 86400  # 24 hours
```

---

## 🎯 Khuyến nghị theo use case

### Cho Development/Testing:
✅ Dùng YouTube để test (không bị block)  
✅ Dùng Instagram (ít bị block hơn TikTok)  
✅ TikTok: test với VPN  

### Cho Production:
✅ Deploy trên VPS nước ngoài (US/EU)  
✅ Sử dụng proxy service  
✅ Implement retry logic  
✅ Cache tích cực (Redis)  
✅ Rate limiting thấp  

---

## 📞 Vẫn không work?

### Check logs:
```bash
python app.py
# Xem error messages trong console
```

### Test với Python script:
```python
import yt_dlp

url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

ydl_opts = {
    'quiet': False,  # Show all logs
    'verbose': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    print(f"Title: {info['title']}")
    print(f"URL: {info['url']}")
```

---

## ✅ Quick Fix Checklist

- [ ] Backend đang chạy? (`http://localhost:8000/health`)
- [ ] Frontend đang chạy? (`http://localhost:3000`)
- [ ] Đã cài đủ dependencies? (`pip install -r requirements.txt`)
- [ ] Test với YouTube trước? (easiest)
- [ ] Check console logs? (F12 trong browser)
- [ ] Thử video khác? (có thể video đó bị restrict)
- [ ] Dùng VPN? (nếu test TikTok)

---

**Made by:** Rovo Dev  
**Last updated:** 2026-02-05
