#!/usr/bin/env python3
"""
Script test API với các platform khác nhau
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

# Test URLs cho từng platform
TEST_URLS = {
    "TikTok": "https://www.tiktok.com/@user/video/123",
    "YouTube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "Instagram": "https://www.instagram.com/reel/ABC123/",
    "Facebook": "https://www.facebook.com/reel/123456789",
}

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        data = response.json()
        print(f"✅ Health Check: {data['status']}")
        print(f"   Cache size: {data['cache_size']}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_download(platform, url, quality="best"):
    """Test download endpoint"""
    print(f"\n🎥 Testing {platform}...")
    try:
        response = requests.post(
            f"{API_URL}/api/download",
            json={"url": url, "quality": quality},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"   Title: {data['title'][:50]}...")
            print(f"   Author: {data['author']}")
            print(f"   Quality: {data['quality']}")
            print(f"   Format: {data['format']}")
            print(f"   No Watermark: {data['no_watermark']}")
            print(f"   Cached: {data['cached']}")
            return True
        else:
            error = response.json()
            print(f"❌ Failed: {error.get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Testing Multi-Platform Video Downloader API")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Server is not running!")
        print("Please start server with: python app.py")
        return
    
    # Test stats
    print("\n📊 Testing Stats Endpoint...")
    try:
        response = requests.get(f"{API_URL}/stats")
        data = response.json()
        print(f"✅ Stats:")
        print(f"   Cached items: {data['total_cached_items']}")
        print(f"   Active clients: {data['active_clients']}")
    except Exception as e:
        print(f"⚠️  Stats endpoint error: {e}")
    
    # Test downloads
    print("\n" + "=" * 60)
    print("Testing Download Functionality")
    print("=" * 60)
    
    results = {}
    for platform, url in TEST_URLS.items():
        result = test_download(platform, url)
        results[platform] = result
        time.sleep(1)  # Rate limiting
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for platform, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {platform}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
