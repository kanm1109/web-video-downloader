# 🚀 Hướng dẫn Deploy Production

Hướng dẫn chi tiết deploy website video downloader lên production.

---

## 📋 Mục lục

1. [Deploy miễn phí (Vercel + Railway)](#deploy-miễn-phí)
2. [Deploy trên VPS](#deploy-trên-vps)
3. [Setup domain & SSL](#setup-domain--ssl)
4. [Tối ưu hóa](#tối-ưu-hóa)

---

## 🆓 Deploy miễn phí (Vercel + Railway)

### Bước 1: Deploy Backend trên Railway

1. **Tạo tài khoản Railway:**
   - Truy cập: https://railway.app
   - Sign up với GitHub

2. **Deploy project:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Deploy
   cd multi-platform-video-downloader
   railway init
   railway up
   ```

3. **Cấu hình environment:**
   - Vào Railway Dashboard
   - Click vào project → Variables
   - Thêm:
     ```
     HOST=0.0.0.0
     PORT=8000
     DEBUG=False
     MAX_REQUESTS_PER_MINUTE=30
     ```

4. **Copy Railway URL:**
   - VD: `https://your-app.up.railway.app`

### Bước 2: Deploy Frontend trên Vercel

1. **Cập nhật API_URL trong index.html:**
   ```javascript
   const API_URL = 'https://your-app.up.railway.app';
   ```

2. **Deploy:**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   vercel
   ```

3. **Hoặc deploy qua GitHub:**
   - Push code lên GitHub
   - Truy cập vercel.com → Import project
   - Chọn repository
   - Deploy!

**Tổng chi phí: $0/tháng** ✅

---

## 🖥️ Deploy trên VPS (Hetzner/DigitalOcean)

### Bước 1: Thuê VPS

**Khuyến nghị Hetzner:**
- Server: CPX11 (2 vCPU, 2GB RAM)
- Giá: €4.5/tháng (~$5)
- Bandwidth: 20TB/tháng

**Link:** https://hetzner.com

### Bước 2: Connect & Setup

```bash
# SSH vào server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install python3 python3-pip nginx git -y

# Clone project
git clone <your-repo-url>
cd multi-platform-video-downloader

# Install Python packages
pip3 install -r requirements.txt

# Setup .env
cp .env.example .env
nano .env
```

### Bước 3: Setup Systemd Service

```bash
nano /etc/systemd/system/videodownloader.service
```

Nội dung:

```ini
[Unit]
Description=Video Downloader API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/root/multi-platform-video-downloader
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
systemctl daemon-reload
systemctl start videodownloader
systemctl enable videodownloader
systemctl status videodownloader
```

### Bước 4: Setup Nginx

```bash
nano /etc/nginx/sites-available/videodownloader
```

Nội dung:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /root/multi-platform-video-downloader;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:8000;
    }
}
```

Enable site:

```bash
ln -s /etc/nginx/sites-available/videodownloader /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

---

## 🔒 Setup Domain & SSL

### Bước 1: Trỏ domain về VPS

Vào nhà cung cấp domain (GoDaddy, Namecheap...):

**A Record:**
```
Type: A
Name: @
Value: your-server-ip
TTL: 3600
```

**CNAME (www):**
```
Type: CNAME
Name: www
Value: yourdomain.com
TTL: 3600
```

### Bước 2: Cài SSL (Let's Encrypt)

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renew (tự động gia hạn)
certbot renew --dry-run
```

**Done!** Website giờ có HTTPS ✅

---

## ⚡ Tối ưu hóa

### 1. Enable Gzip Compression

```bash
nano /etc/nginx/nginx.conf
```

Thêm:

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
```

### 2. Setup Cloudflare CDN

1. Truy cập cloudflare.com
2. Add domain
3. Update nameservers
4. Enable "Auto Minify"
5. Enable "Brotli"
6. Cache Level: Standard

### 3. Monitor với PM2 (Alternative)

```bash
# Install PM2
npm install -g pm2

# Run with PM2
pm2 start app.py --name videodownloader --interpreter python3

# Auto-start on reboot
pm2 startup
pm2 save
```

---

**Chi phí VPS:** $5-10/tháng
**Thời gian setup:** 30-60 phút
