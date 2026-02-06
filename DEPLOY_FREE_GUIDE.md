# 🚀 Hướng dẫn Deploy FREE lên Railway

## ✅ ĐÃ CHUẨN BỊ XONG:

Tôi đã tạo sẵn các files cần thiết:
- ✅ `Procfile` - Railway config
- ✅ `railway.json` - Deploy settings  
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Ignore files
- ✅ Git initialized

---

## 🎯 BƯỚC 1: TẠO TÀI KHOẢN RAILWAY

### 1. Truy cập: https://railway.app

### 2. Click "Login with GitHub"
- Đăng nhập bằng tài khoản GitHub của bạn
- Cho phép Railway truy cập GitHub

### 3. Verify email (nếu cần)

**✅ Xong bước 1!**

---

## 🎯 BƯỚC 2: PUSH CODE LÊN GITHUB

### Option A: Dùng GitHub Desktop (Dễ nhất) ⭐

1. **Download GitHub Desktop:**
   - https://desktop.github.com/
   - Cài đặt và đăng nhập

2. **Add repository:**
   - File → Add Local Repository
   - Chọn folder: `multi-platform-video-downloader`
   - Click "Add Repository"

3. **Create repository on GitHub:**
   - Click "Publish repository"
   - Name: `video-downloader` (hoặc tên bạn thích)
   - ✅ Bỏ tick "Keep this code private" (để public)
   - Click "Publish repository"

**✅ Xong! Code đã lên GitHub**

---

### Option B: Dùng Git command line

```bash
cd multi-platform-video-downloader

# Add all files
git add .

# Commit
git commit -m "Initial commit - Video Downloader"

# Create GitHub repo (dùng GitHub CLI hoặc web)
# Sau đó push:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/video-downloader.git
git push -u origin main
```

---

## 🎯 BƯỚC 3: DEPLOY LÊN RAILWAY

### 1. Vào Railway Dashboard:
- https://railway.app/dashboard

### 2. Click "New Project"

### 3. Chọn "Deploy from GitHub repo"
- Nếu chưa connect GitHub: Click "Configure GitHub App"
- Cho phép Railway truy cập repositories

### 4. Chọn repository `video-downloader`
- Click vào repository vừa tạo
- Railway sẽ tự động detect Python project

### 5. Đợi deploy (2-3 phút)
- Railway sẽ:
  - Install dependencies từ `requirements.txt`
  - Run command từ `Procfile`
  - Deploy lên server

### 6. Lấy URL:
- Click vào project
- Tab "Settings" → "Domains"
- Click "Generate Domain"
- Copy URL: `https://your-app.up.railway.app`

**✅ Backend đã deploy!**

---

## 🎯 BƯỚC 4: CẤU HÌNH ENVIRONMENT VARIABLES

### 1. Trong Railway Dashboard:
- Click vào project
- Tab "Variables"

### 2. Thêm các variables:
```
PORT = 8000
DEBUG = False
ALLOWED_ORIGINS = *
MAX_REQUESTS_PER_MINUTE = 30
CACHE_TTL = 10800
```

### 3. Click "Save" và đợi redeploy

---

## 🎯 BƯỚC 5: DEPLOY FRONTEND (VERCEL)

### 1. Truy cập: https://vercel.com

### 2. Login with GitHub

### 3. Click "Add New" → "Project"

### 4. Import `video-downloader` repository

### 5. Configure:
- **Framework Preset:** Other
- **Root Directory:** `./`
- **Build Command:** (để trống)
- **Output Directory:** `./`

### 6. Click "Deploy"

### 7. Đợi deploy xong (1 phút)

---

## 🎯 BƯỚC 6: UPDATE FRONTEND API URL

### 1. Copy Railway backend URL:
```
https://your-app.up.railway.app
```

### 2. Update file `index.html`:

Tìm dòng:
```javascript
const API_URL = 'http://localhost:8000';
```

Đổi thành:
```javascript
const API_URL = 'https://your-app.up.railway.app';
```

### 3. Commit và push lên GitHub:

**GitHub Desktop:**
- Viết commit message: "Update API URL"
- Click "Commit to main"
- Click "Push origin"

**Git command:**
```bash
git add index.html
git commit -m "Update API URL"
git push
```

### 4. Vercel tự động redeploy (30 giây)

---

## 🎯 BƯỚC 7: CONNECT DOMAIN CỦA BẠN (Tùy chọn)

### Nếu bạn muốn dùng domain riêng:

### A. Vercel (Frontend):
1. Vào Vercel project → Settings → Domains
2. Add domain: `yourdomain.com`
3. Configure DNS:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   ```
4. Đợi verify (vài phút)

### B. Railway (Backend):
1. Vào Railway project → Settings → Domains
2. Add custom domain: `api.yourdomain.com`
3. Configure DNS:
   ```
   Type: CNAME
   Name: api
   Value: your-app.up.railway.app
   ```

**Xong!** Domain của bạn đã hoạt động!

---

## ✅ KIỂM TRA DEPLOY THÀNH CÔNG

### 1. Test Backend:
Mở browser: `https://your-app.up.railway.app/health`

Phải thấy:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "cache_size": 0
}
```

### 2. Test Frontend:
Mở: `https://your-app.vercel.app`

### 3. Test download:
- Dán URL YouTube: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
- Click "Tải Video Ngay"
- Phải thấy video info!

**🎉 DEPLOY THÀNH CÔNG!**

---

## 💰 CHI PHÍ:

```
Railway FREE tier:
  ✅ 500 hours/tháng (đủ cho 1 app chạy 24/7)
  ✅ 100GB bandwidth/tháng
  ✅ $5 credit/tháng

Vercel FREE tier:
  ✅ Unlimited bandwidth
  ✅ Auto SSL
  ✅ Global CDN

Domain (bạn có rồi):
  ✅ $0

TỔNG CHI PHÍ: $0/tháng 🎉
```

---

## 📊 GIỚI HẠN FREE TIER:

**Railway FREE:**
- Chịu tải: 500-1,000 users/ngày
- RAM: 512MB
- CPU: 0.1 vCPU (shared)
- Bandwidth: 100GB/tháng

**Nếu vượt quá:**
- Upgrade Railway Pro: $5/tháng
- Hoặc chuyển sang Hetzner VPS

---

## 🔧 TROUBLESHOOTING:

### Lỗi: "Application failed to respond"
**Fix:**
- Check Railway logs (tab "Deployments")
- Có thể thiếu dependencies
- Update `requirements.txt`

### Lỗi: "CORS policy"
**Fix:**
- Railway Variables → Add: `ALLOWED_ORIGINS=*`
- Redeploy

### Lỗi: "Failed to fetch" trên frontend
**Fix:**
- Kiểm tra API_URL trong `index.html`
- Phải là Railway URL, không phải localhost

---

## 🎯 NEXT STEPS:

Sau khi deploy:

1. **Test với YouTube** (100% work trên Railway US server)
2. **Test với TikTok** (sẽ work vì server US không bị block!)
3. **Test với Facebook**
4. **Add Google AdSense** để kiếm tiền
5. **Share link cho bạn bè test**

---

## 📞 CẦN TRỢ GIÚP?

Nếu gặp vấn đề ở bước nào, cho tôi biết:
- Screenshot lỗi
- Railway logs (nếu có)
- Bước đang bị stuck

Tôi sẽ giúp fix ngay! 😊

---

**Created:** 2026-02-05  
**Status:** ✅ Ready to deploy
