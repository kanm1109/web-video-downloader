# 🎥 Multi-Platform Video Downloader

Tải video không logo, chất lượng cao từ **TikTok, Facebook Reels, Instagram Reels, YouTube, Douyin**

![Platforms](https://img.shields.io/badge/Platforms-TikTok%20%7C%20Facebook%20%7C%20Instagram%20%7C%20YouTube%20%7C%20Douyin-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Tính năng

- ✅ **Không có logo/watermark** - Tải video gốc từ server nền tảng
- ✅ **Chất lượng cao** - Hỗ trợ HD, Full HD, 4K
- ✅ **5 nền tảng** - TikTok, Facebook, Instagram, YouTube, Douyin
- ✅ **Nhanh chóng** - Xử lý trong vài giây với yt-dlp
- ✅ **Cache thông minh** - Giảm tải server, tăng tốc độ
- ✅ **Rate limiting** - Bảo vệ server khỏi spam
- ✅ **API RESTful** - Dễ dàng tích hợp
- ✅ **Responsive UI** - Hoạt động tốt trên mọi thiết bị

---

## 📸 Screenshots

### Desktop View
```
┌─────────────────────────────────────────────┐
│  🎯 VideoDownloader                         │
│  ┌─────────────────────────────────────┐   │
│  │ Dán link video vào đây              │   │
│  │ https://tiktok.com/@user/video/123  │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │ Chất lượng: [Tốt nhất (HD) ▼]      │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │      📥 Tải Video Ngay              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 🚀 Cài đặt & Chạy

### Yêu cầu hệ thống

- Python 3.8 trở lên
- pip
- (Tùy chọn) Redis cho cache

### Bước 1: Clone repository

```bash
cd multi-platform-video-downloader
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình environment

```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Redis (Optional)
REDIS_ENABLED=False

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=30

# CORS
ALLOWED_ORIGINS=*
```

### Bước 4: Chạy server

```bash
python app.py
```

Server sẽ chạy tại: `http://localhost:8000`

### Bước 5: Mở frontend

Mở file `index.html` trong trình duyệt hoặc serve qua HTTP server:

```bash
# Option 1: Python HTTP server
python -m http.server 3000

# Option 2: Node.js http-server
npx http-server -p 3000

# Option 3: VS Code Live Server extension
# Right-click index.html -> Open with Live Server
```

Frontend sẽ chạy tại: `http://localhost:3000`

---

## 📚 API Documentation

### Endpoint: `POST /api/download`

**Request:**

```json
{
  "url": "https://www.tiktok.com/@user/video/123456789",
  "quality": "best"
}
```

**Response (Success):**

```json
{
  "success": true,
  "platform": "TikTok",
  "title": "Amazing dance video",
  "thumbnail": "https://...",
  "duration": 15,
  "author": "@username",
  "download_url": "https://v16.tiktokcdn.com/...",
  "quality": "1080p",
  "format": "mp4",
  "file_size": 5242880,
  "no_watermark": true,
  "cached": false
}
```

**Response (Error):**

```json
{
  "detail": "Failed to extract video: URL not supported"
}
```

### Quality Options

- `best` - Chất lượng cao nhất có sẵn
- `1080p` - Full HD
- `720p` - HD
- `480p` - SD
- `360p` - Low quality

### Other Endpoints

#### `GET /` - API Info
```bash
curl http://localhost:8000/
```

#### `GET /health` - Health Check
```bash
curl http://localhost:8000/health
```

#### `GET /stats` - API Statistics
```bash
curl http://localhost:8000/stats
```

---

## 🛠️ Cấu trúc Project

```
multi-platform-video-downloader/
├── app.py                 # FastAPI backend
├── index.html             # Frontend UI
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # Documentation
```

---

## 🌐 Deploy lên Production

### Option 1: Vercel (Frontend) + Railway (Backend)

#### Deploy Backend trên Railway:

1. Tạo tài khoản tại [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Chọn repository của bạn
4. Railway tự động detect Python và chạy `app.py`
5. Thêm environment variables:
   ```
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   ALLOWED_ORIGINS=https://yourdomain.com
   ```
6. Copy Railway URL (VD: `https://your-app.up.railway.app`)

#### Deploy Frontend trên Vercel:

1. Tạo tài khoản tại [Vercel.com](https://vercel.com)
2. Click "New Project" → Import repository
3. Cập nhật `API_URL` trong `index.html`:
   ```javascript
   const API_URL = 'https://your-app.up.railway.app';
   ```
4. Deploy!
5. Connect domain của bạn

**Chi phí:** $0/tháng (FREE tier)

---

### Option 2: VPS (Hetzner/DigitalOcean)

#### Cài đặt trên VPS:

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python & dependencies
sudo apt install python3 python3-pip nginx -y

# 3. Clone project
git clone <your-repo>
cd multi-platform-video-downloader

# 4. Install dependencies
pip3 install -r requirements.txt

# 5. Setup systemd service
sudo nano /etc/systemd/system/videodownloader.service
```

**File systemd service:**

```ini
[Unit]
Description=Video Downloader API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/multi-platform-video-downloader
ExecStart=/usr/bin/python3 /path/to/multi-platform-video-downloader/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 6. Start service
sudo systemctl daemon-reload
sudo systemctl start videodownloader
sudo systemctl enable videodownloader

# 7. Setup Nginx reverse proxy
sudo nano /etc/nginx/sites-available/videodownloader
```

**Nginx config:**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location / {
        root /path/to/multi-platform-video-downloader;
        index index.html;
    }
}
```

```bash
# 8. Enable site & restart Nginx
sudo ln -s /etc/nginx/sites-available/videodownloader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 9. Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

**Chi phí:** $5-10/tháng (Hetzner VPS)

---

### Option 3: Docker (Recommended for scaling)

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .env .

EXPOSE 8000

CMD ["python", "app.py"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - REDIS_ENABLED=true
      - REDIS_HOST=redis
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./index.html:/usr/share/nginx/html/index.html
    depends_on:
      - api
    restart: unless-stopped

volumes:
  redis_data:
```

**Run:**

```bash
docker-compose up -d
```

---

## ⚡ Performance & Optimization

### 1. Enable Redis Cache

Redis giúp cache video URLs để tăng tốc độ và giảm tải server:

```bash
# Install Redis
sudo apt install redis-server -y

# Enable Redis in .env
REDIS_ENABLED=True
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 2. CDN (Cloudflare)

1. Trỏ domain về server IP
2. Thêm domain vào Cloudflare
3. Enable "Auto Minify" cho HTML/CSS/JS
4. Enable "Brotli compression"
5. Set Cache Level: Standard

**Kết quả:** Tốc độ tăng 3-5x, băng thông giảm 60%

### 3. Rate Limiting

Đã tích hợp sẵn rate limiting (30 requests/phút/IP). Điều chỉnh trong `.env`:

```env
MAX_REQUESTS_PER_MINUTE=30
```

---

## 🔧 Troubleshooting

### Lỗi: "Failed to extract video"

**Nguyên nhân:** URL không hợp lệ hoặc video riêng tư

**Giải pháp:**
- Kiểm tra URL có đúng format không
- Đảm bảo video là công khai (public)
- Thử URL khác để test

### Lỗi: "Rate limit exceeded"

**Nguyên nhân:** Vượt quá 30 requests/phút

**Giải pháp:**
- Đợi 1 phút rồi thử lại
- Tăng `MAX_REQUESTS_PER_MINUTE` trong `.env` (không khuyến khích)

### Lỗi: "CORS policy"

**Nguyên nhân:** Frontend và Backend chạy khác domain

**Giải pháp:**

Cập nhật `ALLOWED_ORIGINS` trong `.env`:

```env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Video không có thumbnail

**Nguyên nhân:** Một số nền tảng không cung cấp thumbnail

**Giải pháp:** Code đã có placeholder image, không ảnh hưởng chức năng

---

## 📊 Supported Platforms

| Platform | Video | Reels | Stories | No Watermark | HD Quality |
|----------|-------|-------|---------|--------------|------------|
| TikTok | ✅ | N/A | ❌ | ✅ | ✅ |
| Facebook | ✅ | ✅ | ❌ | ✅ | ✅ |
| Instagram | ✅ | ✅ | ❌ | ✅ | ✅ |
| YouTube | ✅ | ✅ | N/A | ✅ | ✅ (up to 4K) |
| Douyin | ✅ | N/A | ❌ | ✅ | ✅ |

**Lưu ý:** Stories thường expire sau 24h nên khó tải

---

## 🤝 Contributing

Contributions are welcome! Để contribute:

1. Fork repository
2. Tạo branch mới: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Mở Pull Request

---

## 📝 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết

---

## ⚠️ Disclaimer

Tool này chỉ dành cho mục đích học tập và sử dụng cá nhân. 

**Lưu ý quan trọng:**
- ✅ Tải video để xem cá nhân
- ✅ Backup nội dung của chính bạn
- ⚠️ Tôn trọng bản quyền của creator
- ❌ Không re-upload lên nền tảng khác
- ❌ Không sử dụng thương mại mà không có permission

**Respect creators!** 🙏

---

## 📞 Support

Nếu bạn gặp vấn đề hoặc có câu hỏi:

- 📧 Email: your-email@example.com
- 💬 GitHub Issues: [Create an issue](https://github.com/yourusername/repo/issues)
- 🌐 Website: https://yourdomain.com

---

## 🌟 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Amazing video downloader library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

## 📈 Roadmap

- [ ] Thêm hỗ trợ Twitter/X videos
- [ ] Batch download (nhiều video cùng lúc)
- [ ] Video converter (MP4 to MP3)
- [ ] Browser extension
- [ ] Mobile app (React Native)
- [ ] Playlist downloader
- [ ] Subtitle downloader

---

**Made with ❤️ for video lovers**

⭐ Star this repo if you find it helpful!
