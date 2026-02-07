#!/usr/bin/env python3
"""
Multi-Platform Video Downloader API
Supports: TikTok, Facebook Reels, Instagram Reels, YouTube, Douyin
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, validator
import yt_dlp
import re
import os
import time
import hashlib
from typing import Optional, Dict, List
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Multi-Platform Video Downloader",
    description="Download videos from TikTok, Facebook, Instagram, YouTube, Douyin without watermark",
    version="1.0.0"
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting storage (in-memory for simplicity, use Redis in production)
request_history: Dict[str, List[float]] = {}
MAX_REQUESTS = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "30"))

# Cache storage (in-memory, use Redis in production)
cache: Dict[str, Dict] = {}
CACHE_TTL = int(os.getenv("CACHE_TTL", "10800"))  # 3 hours


class VideoRequest(BaseModel):
    url: str
    quality: Optional[str] = "best"  # best, 1080p, 720p, 480p, 360p
    
    @validator('url')
    def validate_url(cls, v):
        """Validate if URL is from supported platforms"""
        supported_patterns = [
            r'tiktok\.com',
            r'facebook\.com/reel',
            r'fb\.watch',
            r'instagram\.com/reel',
            r'youtube\.com|youtu\.be',
            r'douyin\.com',
        ]
        
        if not any(re.search(pattern, v, re.IGNORECASE) for pattern in supported_patterns):
            raise ValueError('URL must be from TikTok, Facebook Reels, Instagram Reels, YouTube, or Douyin')
        
        return v


class VideoResponse(BaseModel):
    success: bool
    platform: str
    title: str
    thumbnail: Optional[str]
    duration: Optional[int]
    author: Optional[str]
    download_url: str
    quality: str
    format: str
    file_size: Optional[int]
    no_watermark: bool
    cached: bool


def get_cache_key(url: str, quality: str) -> str:
    """Generate cache key from URL and quality"""
    return hashlib.md5(f"{url}_{quality}".encode()).hexdigest()


def check_cache(cache_key: str) -> Optional[Dict]:
    """Check if result is in cache and not expired"""
    if cache_key in cache:
        cached_data = cache[cache_key]
        if time.time() - cached_data['timestamp'] < CACHE_TTL:
            logger.info(f"Cache hit for key: {cache_key}")
            return cached_data['data']
        else:
            # Remove expired cache
            del cache[cache_key]
            logger.info(f"Cache expired for key: {cache_key}")
    return None


def set_cache(cache_key: str, data: Dict):
    """Store result in cache"""
    cache[cache_key] = {
        'data': data,
        'timestamp': time.time()
    }
    logger.info(f"Cached data for key: {cache_key}")


def rate_limit_check(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    current_time = time.time()
    
    # Clean old entries
    if client_ip in request_history:
        request_history[client_ip] = [
            req_time for req_time in request_history[client_ip]
            if current_time - req_time < 60
        ]
    else:
        request_history[client_ip] = []
    
    # Check limit
    if len(request_history[client_ip]) >= MAX_REQUESTS:
        return False
    
    # Add current request
    request_history[client_ip].append(current_time)
    return True


def detect_platform(url: str) -> str:
    """Detect platform from URL"""
    if 'tiktok.com' in url.lower():
        return 'TikTok'
    elif 'douyin.com' in url.lower():
        return 'Douyin'
    elif 'facebook.com' in url.lower() or 'fb.watch' in url.lower():
        return 'Facebook'
    elif 'instagram.com' in url.lower():
        return 'Instagram'
    elif 'youtube.com' in url.lower() or 'youtu.be' in url.lower():
        return 'YouTube'
    return 'Unknown'


def get_format_selector(quality: str, platform: str) -> str:
    """Get format selector based on quality and platform"""
    
    # TikTok/Douyin: prefer no watermark version
    if platform in ['TikTok', 'Douyin']:
        if quality == 'best':
            return 'best[ext=mp4]/best'
        else:
            height = quality.replace('p', '')
            return f'best[height<={height}][ext=mp4]/best[height<={height}]'
    
    # YouTube: prefer single file format (no merge needed)
    elif platform == 'YouTube':
        if quality == 'best':
            return 'best[ext=mp4]/best'
        else:
            height = quality.replace('p', '')
            return f'best[height<={height}][ext=mp4]/best[height<={height}]/best'
    
    # Instagram/Facebook: best available
    else:
        if quality == 'best':
            return 'best[ext=mp4]/best'
        else:
            height = quality.replace('p', '')
            return f'best[height<={height}][ext=mp4]/best[height<={height}]'


def extract_video_info(url: str, quality: str = 'best') -> Dict:
    """Extract video information using yt-dlp"""
    
    platform = detect_platform(url)
    logger.info(f"Processing {platform} URL: {url}")
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': get_format_selector(quality, platform),
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,  # Don't download, just get info
        'nocheckcertificate': True,
        'socket_timeout': 20,  # Add timeout
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
    }
    
    # Platform-specific configurations
    if platform == 'TikTok':
        ydl_opts.update({
            'cookiefile': None,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.tiktok.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            'extractor_args': {
                'tiktok': {
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    'webpage_url_basename': 'video'
                }
            }
        })
    
    elif platform == 'Douyin':
        ydl_opts.update({
            'geo_bypass': True,
            'geo_bypass_country': 'CN',
        })
    
    elif platform == 'Instagram':
        ydl_opts.update({
            'cookiefile': None,
        })
    
    elif platform == 'Facebook':
        ydl_opts.update({
            'format': 'best[ext=mp4]/best',
            'extractor_args': {
                'facebook': {
                    'skip_dash': True
                }
            }
        })
    
    elif platform == 'YouTube':
        ydl_opts.update({
            'format': get_format_selector(quality, platform),
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['dash', 'hls']
                }
            },
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
            },
        })
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract relevant information
            # Handle both single format and merged formats
            download_url = info.get('url')
            
            # If no direct URL (merged format), get the best single format
            if not download_url or 'manifest' in download_url:
                # Get formats list and find best single file
                formats = info.get('formats', [])
                for fmt in reversed(formats):  # Start from best quality
                    if fmt.get('url') and fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        download_url = fmt['url']
                        break
            
            result = {
                'success': True,
                'platform': platform,
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'author': info.get('uploader') or info.get('creator') or info.get('channel'),
                'download_url': download_url or 'N/A',
                'quality': f"{info.get('height', 'Unknown')}p" if info.get('height') else quality,
                'format': info.get('ext', 'mp4'),
                'file_size': info.get('filesize') or info.get('filesize_approx'),
                'no_watermark': True,  # yt-dlp automatically gets no-watermark version when available
                'cached': False,
            }
            
            return result
            
    except Exception as e:
        logger.error(f"Error extracting video info: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to extract video: {str(e)}")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Multi-Platform Video Downloader API",
        "version": "1.0.0",
        "supported_platforms": [
            "TikTok",
            "Facebook Reels",
            "Instagram Reels",
            "YouTube",
            "Douyin"
        ],
        "endpoints": {
            "download": "/api/download",
            "health": "/health",
            "stats": "/stats"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_size": len(cache)
    }


@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    total_requests = sum(len(requests) for requests in request_history.values())
    return {
        "total_cached_items": len(cache),
        "active_clients": len(request_history),
        "total_requests_last_minute": total_requests,
        "cache_ttl_seconds": CACHE_TTL,
    }


@app.post("/api/download", response_model=VideoResponse)
async def download_video(video_request: VideoRequest, request: Request):
    """
    Download video from supported platforms
    
    - **url**: Video URL from TikTok, Facebook, Instagram, YouTube, or Douyin
    - **quality**: Video quality (best, 1080p, 720p, 480p, 360p)
    
    Returns direct download URL (no watermark when available)
    """
    
    # Get client IP
    client_ip = request.client.host
    
    # Rate limiting
    if not rate_limit_check(client_ip):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {MAX_REQUESTS} requests per minute."
        )
    
    # Check cache
    cache_key = get_cache_key(video_request.url, video_request.quality)
    cached_result = check_cache(cache_key)
    
    if cached_result:
        cached_result['cached'] = True
        return VideoResponse(**cached_result)
    
    # Extract video info
    try:
        result = extract_video_info(video_request.url, video_request.quality)
        
        # Cache the result
        set_cache(cache_key, result)
        
        return VideoResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Cache TTL: {CACHE_TTL} seconds")
    logger.info(f"Rate limit: {MAX_REQUESTS} requests/minute")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
