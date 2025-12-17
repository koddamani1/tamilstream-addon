import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import re
import hashlib
import logging
from datetime import datetime
from api.content_store import add_content, add_torrent, load_content, load_torrents

logger = logging.getLogger(__name__)


def generate_hash(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()


def parse_size(size_str: str) -> tuple:
    size_str = size_str.strip().upper()
    match = re.match(r'([\d.]+)\s*(GB|MB|KB|TB)', size_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        multipliers = {'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
        size_bytes = int(value * multipliers.get(unit, 1))
        return size_bytes, size_str
    return 0, size_str


def detect_quality(title: str) -> str:
    title_upper = title.upper()
    if '2160P' in title_upper or '4K' in title_upper or 'UHD' in title_upper:
        return '4K'
    elif '1080P' in title_upper or 'FULL HD' in title_upper or 'FHD' in title_upper:
        return '1080p'
    elif '720P' in title_upper or 'HD' in title_upper:
        return 'HD'
    elif 'HDCAM' in title_upper:
        return 'HDCAM'
    elif 'CAM' in title_upper or 'CAMRIP' in title_upper:
        return 'CAM'
    elif 'HDTS' in title_upper or 'TS' in title_upper:
        return 'HDTS'
    return 'Unknown'


def extract_year(title: str) -> Optional[int]:
    match = re.search(r'\b(19|20)\d{2}\b', title)
    if match:
        return int(match.group(0))
    return None


def clean_title(title: str) -> str:
    clean = re.sub(r'\b(19|20)\d{2}\b', '', title)
    clean = re.sub(r'\b(720p|1080p|2160p|4K|UHD|HDRip|BluRay|WEB-DL|WEBRip|HDCAM|CAM|DVDRip|x264|x265|HEVC|AAC|Tamil|Hindi|English|Dual Audio|Multi Audio)\b', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'[._\-\[\]()]', ' ', clean)
    clean = ' '.join(clean.split())
    return clean.strip()


def extract_info_hash_from_magnet(magnet: str) -> Optional[str]:
    match = re.search(r'btih:([a-fA-F0-9]{40})', magnet)
    if match:
        return match.group(1).lower()
    match = re.search(r'btih:([a-zA-Z0-9]{32})', magnet)
    if match:
        return match.group(1).lower()
    return None


class TamilContentScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.timeout = 30.0
    
    async def fetch_page(self, url: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    follow_redirects=True
                )
                if response.status_code == 200:
                    return response.text
                logger.warning(f"Failed to fetch {url}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_torrent_entry(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            title = entry.get('title', '')
            magnet = entry.get('magnet', '')
            size_str = entry.get('size', '0 MB')
            
            if not title or not magnet:
                return None
            
            info_hash = extract_info_hash_from_magnet(magnet)
            if not info_hash:
                info_hash = generate_hash(title)
            
            size_bytes, size_readable = parse_size(size_str)
            quality = detect_quality(title)
            year = extract_year(title)
            clean_name = clean_title(title)
            
            content_id = f"tt{generate_hash(clean_name)[:7]}"
            
            return {
                'id': f"torrent_{generate_hash(info_hash)[:8]}",
                'content_id': content_id,
                'info_hash': info_hash,
                'title': title,
                'size': size_bytes,
                'size_readable': size_readable,
                'quality': quality,
                'seeders': entry.get('seeders', 0),
                'leechers': entry.get('leechers', 0),
                'source': entry.get('source', 'Unknown'),
                'magnet': magnet,
                'created_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parsing torrent entry: {e}")
            return None
    
    def create_content_from_torrent(self, torrent: Dict[str, Any]) -> Dict[str, Any]:
        title = clean_title(torrent.get('title', ''))
        year = extract_year(torrent.get('title', ''))
        
        is_series = any(pattern in torrent.get('title', '').upper() 
                       for pattern in ['S01', 'S02', 'SEASON', 'EPISODE', 'EP0', 'EP1'])
        
        return {
            'id': torrent.get('content_id'),
            'imdb_id': torrent.get('content_id'),
            'title': title or torrent.get('title', ''),
            'year': year,
            'type': 'series' if is_series else 'movie',
            'poster': None,
            'description': f"Tamil {'Series' if is_series else 'Movie'} - {title}",
            'genres': ['Tamil'],
            'rating': None,
            'runtime': None,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
    
    async def run_scrape(self) -> Dict[str, int]:
        logger.info("Starting content scrape...")
        
        stats = {
            'new_content': 0,
            'new_torrents': 0,
            'errors': 0
        }
        
        logger.info(f"Scrape completed. Stats: {stats}")
        return stats


async def run_scheduled_scrape():
    scraper = TamilContentScraper()
    try:
        stats = await scraper.run_scrape()
        logger.info(f"Scheduled scrape completed: {stats}")
    except Exception as e:
        logger.error(f"Scheduled scrape failed: {e}")


def setup_scheduler():
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from api.config import settings
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_scheduled_scrape,
        'interval',
        hours=settings.scraper_interval_hours,
        id='tamil_content_scraper',
        replace_existing=True
    )
    return scheduler
