"""
Content store fallback - uses scraped JSON data or in-memory sample data
"""

import os
import json
from typing import Optional, List, Dict, Any

def load_scraped_content():
    """Load scraped content from JSON file if available"""
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "scraped_content.json"),
        os.path.join(os.path.dirname(__file__), "..", "data", "scraped_content.json"),
        "/var/task/data/scraped_content.json",
        "data/scraped_content.json",
    ]
    for json_path in possible_paths:
        try:
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            continue
    return None

SAMPLE_TAMIL_MOVIES = [
    {
        "id": "tt15354916",
        "imdb_id": "tt15354916",
        "title": "Ponniyin Selvan I",
        "year": 2022,
        "type": "movie",
        "description": "Vandiyathevan, a clever and brave warrior, goes on a mission to deliver a message to the Chola king.",
        "genres": ["Action", "Drama", "History"],
        "rating": 7.5,
        "runtime": "167 min"
    },
    {
        "id": "tt21064584",
        "imdb_id": "tt21064584",
        "title": "Jailer",
        "year": 2023,
        "type": "movie",
        "description": "A retired jailer goes on a rampage when his son, an honest cop, is killed by a crime syndicate.",
        "genres": ["Action", "Thriller"],
        "rating": 7.0,
        "runtime": "168 min"
    },
    {
        "id": "tt9900782",
        "imdb_id": "tt9900782",
        "title": "Vikram",
        "year": 2022,
        "type": "movie",
        "description": "A special agent investigates a murder committed by a masked group of serial killers.",
        "genres": ["Action", "Crime", "Thriller"],
        "rating": 8.3,
        "runtime": "174 min"
    },
    {
        "id": "tt6788942",
        "imdb_id": "tt6788942",
        "title": "Master",
        "year": 2021,
        "type": "movie",
        "description": "An alcoholic professor is sent to a juvenile school, where he clashes with a gangster.",
        "genres": ["Action", "Thriller"],
        "rating": 7.2,
        "runtime": "179 min"
    },
    {
        "id": "tt10869796",
        "imdb_id": "tt10869796",
        "title": "Leo",
        "year": 2023,
        "type": "movie",
        "description": "A cafe owner with a dark past takes on a group of gangsters.",
        "genres": ["Action", "Crime", "Drama"],
        "rating": 6.6,
        "runtime": "164 min"
    },
    {
        "id": "tt27524176",
        "imdb_id": "tt27524176",
        "title": "GOAT",
        "year": 2024,
        "type": "movie",
        "description": "A retired special agent returns to action when his family is threatened.",
        "genres": ["Action", "Thriller"],
        "rating": 6.5,
        "runtime": "170 min"
    }
]

SAMPLE_TAMIL_SERIES = [
    {
        "id": "tt15744286",
        "imdb_id": "tt15744286",
        "title": "Suzhal: The Vortex",
        "year": 2022,
        "type": "series",
        "description": "A missing child case in a small town uncovers dark secrets and hidden truths.",
        "genres": ["Crime", "Drama", "Mystery"],
        "rating": 7.3,
        "runtime": "45 min",
        "videos": [
            {"id": "tt15744286:1:1", "title": "Episode 1", "season": 1, "episode": 1},
            {"id": "tt15744286:1:2", "title": "Episode 2", "season": 1, "episode": 2},
            {"id": "tt15744286:1:3", "title": "Episode 3", "season": 1, "episode": 3},
            {"id": "tt15744286:1:4", "title": "Episode 4", "season": 1, "episode": 4}
        ]
    },
    {
        "id": "tt21245112",
        "imdb_id": "tt21245112",
        "title": "The Night Manager",
        "year": 2023,
        "type": "series",
        "description": "A hotel night manager becomes an undercover agent to infiltrate an arms dealer's network.",
        "genres": ["Action", "Drama", "Thriller"],
        "rating": 7.8,
        "runtime": "50 min",
        "videos": [
            {"id": "tt21245112:1:1", "title": "Episode 1", "season": 1, "episode": 1},
            {"id": "tt21245112:1:2", "title": "Episode 2", "season": 1, "episode": 2},
            {"id": "tt21245112:1:3", "title": "Episode 3", "season": 1, "episode": 3}
        ]
    }
]

SAMPLE_TORRENTS = [
    {
        "id": "torrent_1",
        "content_id": "tt15354916",
        "info_hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        "title": "Ponniyin.Selvan.I.2022.Tamil.1080p.BluRay.x264",
        "size": 4294967296,
        "size_readable": "4.0 GB",
        "quality": "1080p",
        "seeders": 150,
        "leechers": 20,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    },
    {
        "id": "torrent_2",
        "content_id": "tt9900782",
        "info_hash": "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
        "title": "Vikram.2022.Tamil.2160p.4K.WEB-DL.x265",
        "size": 8589934592,
        "size_readable": "8.0 GB",
        "quality": "4K",
        "seeders": 100,
        "leechers": 15,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
    }
]

_scraped_data = load_scraped_content()
_content_cache = SAMPLE_TAMIL_MOVIES + SAMPLE_TAMIL_SERIES
_torrents_cache = SAMPLE_TORRENTS

if _scraped_data and (_scraped_data.get("series") or _scraped_data.get("movies")):
    _content_cache = _scraped_data.get("movies", []) + _scraped_data.get("series", [])


def initialize_sample_data():
    pass


def get_all_content(content_type: Optional[str] = None) -> List[Dict[str, Any]]:
    if content_type:
        return [c for c in _content_cache if c.get("type") == content_type]
    return _content_cache


def get_content_by_id(content_id: str) -> Optional[Dict[str, Any]]:
    for c in _content_cache:
        if c.get("id") == content_id or c.get("imdb_id") == content_id:
            return c
    return None


def get_torrents_for_content(content_id: str) -> List[Dict[str, Any]]:
    return [t for t in _torrents_cache if t.get("content_id") == content_id]


def search_content(query: str) -> List[Dict[str, Any]]:
    query_lower = query.lower()
    return [c for c in _content_cache if query_lower in c.get("title", "").lower()]


def update_content_poster(content_id: str, poster_url: str) -> bool:
    return False
