# 🧪 Test URLs - Danh sách link để test

## ✅ YouTube (Luôn hoạt động)

### Video ngắn (test nhanh):
```
https://www.youtube.com/watch?v=jNQXAC9IVRw
Tiêu đề: Me at the zoo (first YouTube video)
Độ dài: 19 giây
```

### YouTube Shorts:
```
https://www.youtube.com/shorts/xxx
(Thay xxx bằng ID bất kỳ)
```

### Video HD:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
Tiêu đề: Rick Astley - Never Gonna Give You Up
Quality: Lên đến 1080p
```

---

## ⚠️ TikTok (Cần VPN hoặc Proxy)

**Vấn đề:** IP bị block ở Việt Nam/một số quốc gia

**Giải pháp tạm thời:**
1. Bật VPN (US/Europe server)
2. Thử lại

**Test URLs:**
```
https://www.tiktok.com/@zachking/video/7086600994846313754
https://vm.tiktok.com/ZMhWgGFD4/
```

---

## 🔓 Instagram Reels (Cần cookies)

**Vấn đề:** Cần đăng nhập

**Giải pháp:**
1. Đăng nhập Instagram trên browser
2. Export cookies (extension: "Get cookies.txt")
3. Add vào code

**Test URLs:**
```
https://www.instagram.com/reel/[REEL_ID]/
(Cần cookies để test)
```

---

## 📘 Facebook (Cần cookies cho private videos)

**Public videos thường work:**
```
https://www.facebook.com/watch?v=xxxxx
https://fb.watch/xxxxx
```

---

## 🌏 Douyin (Cần China VPN)

```
https://www.douyin.com/video/xxxxx
(Cần VPN China hoặc proxy)
```

---

## 🎯 KHUYẾN NGHỊ ĐỂ TEST

### 1. Test với YouTube trước (100% work):
✅ Dễ nhất, không cần VPN/cookies
✅ Nhiều quality options
✅ Nhanh

### 2. Sau đó test Facebook:
✅ Khá ổn định
✅ Ít bị block hơn TikTok

### 3. TikTok/Instagram/Douyin:
⚠️ Cần setup thêm (VPN/cookies/proxy)

---

## 💡 Test ngay trong Frontend

1. Mở: http://localhost:3000
2. Dán URL YouTube: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
3. Chọn quality: `360p` (nhanh nhất)
4. Click "Tải Video Ngay"
5. Xong! ✅

---

## 🔧 Nếu muốn test TikTok:

### Option A: Dùng VPN free
1. Download ProtonVPN (free)
2. Connect tới US server
3. Thử lại TikTok URL

### Option B: Deploy lên server nước ngoài
- Railway (US server) - FREE
- Hetzner (Germany) - $5/tháng
- DigitalOcean (US) - $6/tháng

Khi deploy lên server ngoài, TikTok sẽ work tốt hơn!

---

**Made by:** Rovo Dev
