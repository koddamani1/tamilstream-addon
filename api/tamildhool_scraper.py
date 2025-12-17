"""
TamilDhool Scraper - Scrapes Tamil TV shows and episodes from tamildhool.tech
"""

import urllib.request
import urllib.error
import re
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://www.tamildhool.tech"

CHANNELS = {
    "sun-tv": {"name": "Sun TV", "serials": "/sun-tv/sun-tv-serial/", "shows": "/sun-tv/sun-tv-show/"},
    "vijay-tv": {"name": "Vijay TV", "serials": "/vijay-tv/vijay-tv-serial/", "shows": "/vijay-tv/vijay-tv-show/"},
    "zee-tamil": {"name": "Zee Tamil", "serials": "/zee-tamil/zee-tamil-serial/", "shows": "/zee-tamil/zee-tamil-show/"},
    "kalaignar-tv": {"name": "Kalaignar TV", "serials": "/kalaignar-tv/", "shows": None}
}


def fetch_page(url: str) -> Optional[str]:
    """Fetch a webpage and return its HTML content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


def scrape_show_list(channel_slug: str, content_type: str = "serials") -> List[Dict[str, Any]]:
    """Scrape list of shows from a channel page"""
    shows = []
    
    channel = CHANNELS.get(channel_slug)
    if not channel:
        return shows
    
    path = channel.get(content_type) or channel.get("serials")
    if not path:
        return shows
    
    url = f"{BASE_URL}{path}"
    html = fetch_page(url)
    
    if not html:
        return shows
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        articles = soup.find_all('article')
        
        for article in articles:
            try:
                title_elem = article.find(['h2', 'h3'], class_='entry-title')
                if not title_elem:
                    title_elem = article.find('a', class_='post-title')
                
                link_elem = article.find('a', href=True)
                img_elem = article.find('img', src=True)
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get('href', '')
                    
                    poster = ""
                    if img_elem:
                        poster = img_elem.get('data-src') or img_elem.get('src', '')
                        if poster.startswith('data:'):
                            poster = img_elem.get('data-src', '')
                    
                    show_id = link.rstrip('/').split('/')[-1]
                    
                    shows.append({
                        "id": f"td_{show_id}",
                        "title": title,
                        "url": link,
                        "poster": poster,
                        "channel": channel["name"],
                        "type": "series"
                    })
            except Exception as e:
                logger.debug(f"Error parsing article: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error parsing show list: {e}")
    
    return shows


def scrape_latest_episodes(limit: int = 20) -> List[Dict[str, Any]]:
    """Scrape latest episodes from homepage"""
    episodes = []
    
    html = fetch_page(BASE_URL)
    if not html:
        return episodes
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        posts = soup.find_all('article', class_='post')
        
        for post in posts[:limit]:
            try:
                title_elem = post.find(['h2', 'h3'], class_='entry-title')
                if not title_elem:
                    title_elem = post.find('a')
                
                link_elem = post.find('a', href=True)
                img_elem = post.find('img')
                date_elem = post.find('time') or post.find(class_='entry-date')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get('href', '')
                    
                    poster = ""
                    if img_elem:
                        poster = img_elem.get('data-src') or img_elem.get('src', '')
                        if poster.startswith('data:'):
                            poster = img_elem.get('data-src', '')
                    
                    date_str = ""
                    if date_elem:
                        date_str = date_elem.get('datetime', '') or date_elem.get_text(strip=True)
                    
                    episode_id = link.rstrip('/').split('/')[-1]
                    
                    episodes.append({
                        "id": f"td_ep_{episode_id}",
                        "title": title,
                        "url": link,
                        "poster": poster,
                        "date": date_str,
                        "type": "episode"
                    })
            except Exception as e:
                logger.debug(f"Error parsing post: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error parsing latest episodes: {e}")
    
    return episodes


def scrape_episode_details(episode_url: str) -> Optional[Dict[str, Any]]:
    """Scrape episode details and video sources from an episode page"""
    html = fetch_page(episode_url)
    if not html:
        return None
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        title = ""
        title_elem = soup.find('h1', class_='entry-title')
        if title_elem:
            title = title_elem.get_text(strip=True)
        
        video_sources = []
        
        iframes = soup.find_all('iframe', src=True)
        for iframe in iframes:
            src = iframe.get('src', '')
            if src and ('player' in src.lower() or 'video' in src.lower() or 'embed' in src.lower()):
                video_sources.append({
                    "type": "iframe",
                    "url": src
                })
        
        video_tags = soup.find_all('video')
        for video in video_tags:
            source = video.find('source', src=True)
            if source:
                video_sources.append({
                    "type": "direct",
                    "url": source.get('src', '')
                })
        
        player_divs = soup.find_all('div', class_=re.compile(r'player|video', re.I))
        for div in player_divs:
            data_src = div.get('data-src') or div.get('data-video')
            if data_src:
                video_sources.append({
                    "type": "data",
                    "url": data_src
                })
        
        return {
            "title": title,
            "url": episode_url,
            "video_sources": video_sources
        }
        
    except Exception as e:
        logger.error(f"Error parsing episode details: {e}")
        return None


def scrape_all_shows() -> List[Dict[str, Any]]:
    """Scrape all shows from all channels"""
    all_shows = []
    
    for channel_slug in CHANNELS:
        logger.info(f"Scraping {channel_slug}...")
        
        serials = scrape_show_list(channel_slug, "serials")
        all_shows.extend(serials)
        
        shows = scrape_show_list(channel_slug, "shows")
        all_shows.extend(shows)
    
    return all_shows


def convert_to_stremio_format(shows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert scraped shows to Stremio catalog format"""
    stremio_content = []
    
    for show in shows:
        content = {
            "id": show["id"],
            "imdb_id": show["id"],
            "title": show["title"],
            "type": "series",
            "poster": show.get("poster", ""),
            "description": f"Tamil TV Series from {show.get('channel', 'TamilDhool')}",
            "genres": ["Tamil", "Drama", show.get("channel", "TV")],
            "source_url": show.get("url", "")
        }
        stremio_content.append(content)
    
    return stremio_content


def save_scraped_content():
    """Scrape all content and save to JSON file for Vercel"""
    import os
    
    logger.info("Starting full scrape...")
    
    all_shows = scrape_all_shows()
    logger.info(f"Found {len(all_shows)} shows")
    
    stremio_series = convert_to_stremio_format(all_shows)
    
    latest_episodes = scrape_latest_episodes(50)
    logger.info(f"Found {len(latest_episodes)} latest episodes")
    
    data = {
        "movies": [],
        "series": stremio_series,
        "episodes": latest_episodes,
        "last_updated": datetime.now().isoformat()
    }
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    json_path = os.path.join(data_dir, "scraped_content.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved content to {json_path}")
    return data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    save_scraped_content()
