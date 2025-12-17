import urllib.request
import urllib.error
import json
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "")
OMDB_BASE_URL = "http://www.omdbapi.com/"


async def fetch_metadata_for_imdb(imdb_id: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata including poster from external APIs based on IMDB ID"""
    
    metadata = await fetch_from_omdb(imdb_id)
    if metadata and metadata.get("poster"):
        return metadata
    
    if TMDB_API_KEY:
        tmdb_metadata = await fetch_from_tmdb(imdb_id)
        if tmdb_metadata:
            return tmdb_metadata
    
    return metadata


async def fetch_from_omdb(imdb_id: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from OMDb API (free, supports IMDB IDs directly)"""
    try:
        api_key = OMDB_API_KEY or "trilogy"
        url = f"{OMDB_BASE_URL}?i={imdb_id}&apikey={api_key}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'TamilStream/1.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        if data.get("Response") == "True":
            poster = data.get("Poster", "")
            if poster and poster != "N/A":
                return {
                    "poster": poster,
                    "title": data.get("Title"),
                    "year": data.get("Year"),
                    "description": data.get("Plot"),
                    "rating": data.get("imdbRating"),
                    "genres": data.get("Genre", "").split(", ") if data.get("Genre") else [],
                    "runtime": data.get("Runtime")
                }
    except Exception as e:
        logger.debug(f"OMDb fetch failed for {imdb_id}: {e}")
    
    return None


async def fetch_from_tmdb(imdb_id: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from TMDB API"""
    if not TMDB_API_KEY:
        return None
    
    try:
        url = f"{TMDB_BASE_URL}/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'TamilStream/1.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        result = None
        if data.get("movie_results"):
            result = data["movie_results"][0]
        elif data.get("tv_results"):
            result = data["tv_results"][0]
        
        if result and result.get("poster_path"):
            return {
                "poster": f"{TMDB_IMAGE_BASE}{result['poster_path']}",
                "background": f"{TMDB_IMAGE_BASE}{result.get('backdrop_path', result['poster_path'])}",
                "title": result.get("title") or result.get("name"),
                "description": result.get("overview"),
                "rating": result.get("vote_average")
            }
    except Exception as e:
        logger.debug(f"TMDB fetch failed for {imdb_id}: {e}")
    
    return None


def get_poster_for_imdb_sync(imdb_id: str) -> Optional[str]:
    """Synchronous version to get poster URL"""
    try:
        api_key = OMDB_API_KEY or "trilogy"
        url = f"{OMDB_BASE_URL}?i={imdb_id}&apikey={api_key}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'TamilStream/1.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        if data.get("Response") == "True":
            poster = data.get("Poster", "")
            if poster and poster != "N/A":
                return poster
    except Exception as e:
        logger.debug(f"Poster fetch failed for {imdb_id}: {e}")
    
    return None
