#!/usr/bin/env python3
"""
Simple test script - Test yt-dlp trực tiếp không qua API
"""

import yt_dlp
import sys

def test_youtube():
    """Test YouTube - Luôn work"""
    print("\n" + "="*50)
    print("🧪 Testing YouTube...")
    print("="*50)
    
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    ydl_opts = {
        'format': 'best[height<=360]',  # Low quality for fast test
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"\n✅ SUCCESS!")
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            print(f"Quality: {info.get('height', 'N/A')}p")
            print(f"Format: {info.get('ext', 'N/A')}")
            print(f"Download URL: {info.get('url', 'N/A')[:80]}...")
            return True
            
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_instagram():
    """Test Instagram Reel"""
    print("\n" + "="*50)
    print("🧪 Testing Instagram Reel...")
    print("="*50)
    
    url = "https://www.instagram.com/reel/C2KqXXXXXXX/"  # Example
    
    ydl_opts = {
        'format': 'best',
        'quiet': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"\n✅ SUCCESS!")
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Author: {info.get('uploader', 'N/A')}")
            return True
            
    except Exception as e:
        print(f"\n⚠️ Instagram test skipped (need valid URL)")
        print(f"Error: {e}")
        return None


def test_tiktok():
    """Test TikTok - Có thể bị block"""
    print("\n" + "="*50)
    print("🧪 Testing TikTok...")
    print("="*50)
    print("⚠️  Note: TikTok may block your IP")
    
    url = "https://www.tiktok.com/@zachking/video/7086600994846313754"
    
    ydl_opts = {
        'format': 'best',
        'quiet': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"\n✅ SUCCESS!")
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Author: {info.get('uploader', 'N/A')}")
            return True
            
    except Exception as e:
        print(f"\n⚠️ TikTok blocked (expected)")
        print(f"Error: {str(e)[:100]}...")
        print(f"\n💡 Solution: Use VPN or proxy")
        return False


def main():
    print("="*50)
    print("🔍 yt-dlp Direct Test")
    print("="*50)
    print("Testing video extraction without API...")
    
    results = {
        'YouTube': test_youtube(),
        'Instagram': test_instagram(),
        'TikTok': test_tiktok(),
    }
    
    print("\n" + "="*50)
    print("📊 Test Summary")
    print("="*50)
    
    for platform, result in results.items():
        if result is True:
            print(f"✅ {platform}: PASS")
        elif result is False:
            print(f"❌ {platform}: FAIL")
        else:
            print(f"⏭️  {platform}: SKIPPED")
    
    print("\n" + "="*50)
    
    # Recommendations
    if results['YouTube']:
        print("\n✅ YouTube works! Use it for testing.")
        print("💡 Your frontend should work with YouTube URLs")
    else:
        print("\n❌ Something is wrong with yt-dlp installation")
        print("Try: pip install --upgrade yt-dlp")
    
    if not results['TikTok']:
        print("\n⚠️  TikTok IP blocked (common issue)")
        print("Solutions:")
        print("  1. Use VPN")
        print("  2. Use proxy service")
        print("  3. Deploy on foreign VPS")
        print("  4. Test with other platforms first")
    
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
