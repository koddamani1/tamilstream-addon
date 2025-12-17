from typing import Optional, List, Dict, Any
from datetime import datetime
from api.models import TamilContent, TorrentInfo, ContentType, StreamQuality
import json
import os

CONTENT_FILE = "data/content.json"
TORRENTS_FILE = "data/torrents.json"


def ensure_data_dir():
    os.makedirs("data", exist_ok=True)


def load_content() -> List[Dict[str, Any]]:
    ensure_data_dir()
    if os.path.exists(CONTENT_FILE):
        try:
            with open(CONTENT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_content(content: List[Dict[str, Any]]):
    ensure_data_dir()
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, default=str)


def load_torrents() -> List[Dict[str, Any]]:
    ensure_data_dir()
    if os.path.exists(TORRENTS_FILE):
        try:
            with open(TORRENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_torrents(torrents: List[Dict[str, Any]]):
    ensure_data_dir()
    with open(TORRENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(torrents, f, indent=2, default=str)


SAMPLE_TAMIL_MOVIES = [
    {
        "id": "tt15354916",
        "imdb_id": "tt15354916",
        "title": "Ponniyin Selvan I",
        "year": 2022,
        "type": "movie",
        "poster": "https://m.media-amazon.com/images/M/MV5BNmJlMWEzZGMtMGYxZS00ZTliLThlMDEtY2IyMGM3Y2M5NDI0XkEyXkFqcGdeQXVyMTU0ODI1NTA2._V1_.jpg",
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
        "poster": "https://m.media-amazon.com/images/M/MV5BYzYzZDRhNzctZjBlYi00OGI3LWJjNGMtN2M2ZTA0OGM1ZTY3XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",
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
        "poster": "https://m.media-amazon.com/images/M/MV5BOWFlZmQ0OTYtNTg2YS00YmM0LTlmNjEtNmY0MjI4MDAyNDIzXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",
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
        "poster": "https://m.media-amazon.com/images/M/MV5BYzg0YmZjYWQtZjBjYS00YTQxLTk1ZmUtNGY0NzkxYWE2NDkxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
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
        "poster": "https://m.media-amazon.com/images/M/MV5BMDQxNzNiMGItNjM5OC00YmNjLWJkNDUtN2E0OGFhYjgzYmViXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",
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
        "poster": "https://m.media-amazon.com/images/M/MV5BOGZiYmY2MjktMjViYi00YWQ3LTk4NjctMWM5MGQyNDg0NDBjXkEyXkFqcGc@._V1_.jpg",
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
        "poster": "https://m.media-amazon.com/images/M/MV5BN2ExYWY1ZmYtMGE0NC00MDQ5LTk0ODMtNDhkNzZkNGE3ZmQ5XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",
        "description": "When a young girl goes missing in an industrial Tamil town, two cops must work together to find her.",
        "genres": ["Crime", "Drama", "Mystery"],
        "rating": 7.8,
        "runtime": "45 min",
        "videos": [
            {"id": "tt15744286:1:1", "title": "Episode 1", "season": 1, "episode": 1, "released": "2022-06-17"},
            {"id": "tt15744286:1:2", "title": "Episode 2", "season": 1, "episode": 2, "released": "2022-06-17"},
            {"id": "tt15744286:1:3", "title": "Episode 3", "season": 1, "episode": 3, "released": "2022-06-17"},
            {"id": "tt15744286:1:4", "title": "Episode 4", "season": 1, "episode": 4, "released": "2022-06-17"},
            {"id": "tt15744286:1:5", "title": "Episode 5", "season": 1, "episode": 5, "released": "2022-06-17"},
            {"id": "tt15744286:1:6", "title": "Episode 6", "season": 1, "episode": 6, "released": "2022-06-17"},
            {"id": "tt15744286:1:7", "title": "Episode 7", "season": 1, "episode": 7, "released": "2022-06-17"},
            {"id": "tt15744286:1:8", "title": "Episode 8", "season": 1, "episode": 8, "released": "2022-06-17"}
        ]
    },
    {
        "id": "tt21245112",
        "imdb_id": "tt21245112",
        "title": "The Night Manager",
        "year": 2023,
        "type": "series",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjY5MmVlYzQtYmNjNi00MGNjLTg0YTAtNWFhNjRhYzlhMTg5XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",
        "description": "An undercover agent goes deep into an arms dealer's network in this Tamil adaptation.",
        "genres": ["Action", "Crime", "Drama"],
        "rating": 7.4,
        "runtime": "50 min",
        "videos": [
            {"id": "tt21245112:1:1", "title": "Episode 1", "season": 1, "episode": 1, "released": "2023-02-17"},
            {"id": "tt21245112:1:2", "title": "Episode 2", "season": 1, "episode": 2, "released": "2023-02-17"},
            {"id": "tt21245112:1:3", "title": "Episode 3", "season": 1, "episode": 3, "released": "2023-02-17"},
            {"id": "tt21245112:1:4", "title": "Episode 4", "season": 1, "episode": 4, "released": "2023-02-24"},
            {"id": "tt21245112:1:5", "title": "Episode 5", "season": 1, "episode": 5, "released": "2023-02-24"},
            {"id": "tt21245112:1:6", "title": "Episode 6", "season": 1, "episode": 6, "released": "2023-02-24"},
            {"id": "tt21245112:1:7", "title": "Episode 7", "season": 1, "episode": 7, "released": "2023-03-03"}
        ]
    },
    {
        "id": "tt11427016",
        "imdb_id": "tt11427016",
        "title": "November Story",
        "year": 2021,
        "type": "series",
        "poster": "https://m.media-amazon.com/images/M/MV5BZDhjMjdlNjMtNGQ3MC00YjI3LWE5YjctNWJhODAxNjhkYTg5XkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",
        "description": "A hacker tries to clear her father's name when he is accused of murder.",
        "genres": ["Crime", "Drama", "Mystery"],
        "rating": 8.0,
        "runtime": "40 min",
        "videos": [
            {"id": "tt11427016:1:1", "title": "Episode 1", "season": 1, "episode": 1, "released": "2021-05-20"},
            {"id": "tt11427016:1:2", "title": "Episode 2", "season": 1, "episode": 2, "released": "2021-05-20"},
            {"id": "tt11427016:1:3", "title": "Episode 3", "season": 1, "episode": 3, "released": "2021-05-20"},
            {"id": "tt11427016:1:4", "title": "Episode 4", "season": 1, "episode": 4, "released": "2021-05-20"},
            {"id": "tt11427016:1:5", "title": "Episode 5", "season": 1, "episode": 5, "released": "2021-05-20"},
            {"id": "tt11427016:1:6", "title": "Episode 6", "season": 1, "episode": 6, "released": "2021-05-20"},
            {"id": "tt11427016:1:7", "title": "Episode 7", "season": 1, "episode": 7, "released": "2021-05-20"}
        ]
    }
]

SAMPLE_TORRENTS = [
    {
        "id": "torrent_1",
        "content_id": "tt15354916",
        "info_hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        "title": "Ponniyin.Selvan.I.2022.Tamil.1080p.WEB-DL.x264",
        "size": 3221225472,
        "size_readable": "3.0 GB",
        "quality": "1080p",
        "seeders": 150,
        "leechers": 20,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2&dn=Ponniyin.Selvan.I.2022.Tamil.1080p.WEB-DL.x264"
    },
    {
        "id": "torrent_2",
        "content_id": "tt21064584",
        "info_hash": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        "title": "Jailer.2023.Tamil.1080p.WEB-DL.x264",
        "size": 3758096384,
        "size_readable": "3.5 GB",
        "quality": "1080p",
        "seeders": 200,
        "leechers": 30,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3&dn=Jailer.2023.Tamil.1080p.WEB-DL.x264"
    },
    {
        "id": "torrent_3",
        "content_id": "tt9900782",
        "info_hash": "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
        "title": "Vikram.2022.Tamil.2160p.4K.WEB-DL.x265",
        "size": 8589934592,
        "size_readable": "8.0 GB",
        "quality": "4K",
        "seeders": 100,
        "leechers": 15,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4&dn=Vikram.2022.Tamil.2160p.4K.WEB-DL.x265"
    },
    {
        "id": "torrent_4",
        "content_id": "tt6788942",
        "info_hash": "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5",
        "title": "Master.2021.Tamil.720p.WEB-DL.x264",
        "size": 1610612736,
        "size_readable": "1.5 GB",
        "quality": "HD",
        "seeders": 80,
        "leechers": 10,
        "source": "TamilBlasters",
        "magnet": "magnet:?xt=urn:btih:d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5&dn=Master.2021.Tamil.720p.WEB-DL.x264"
    },
    {
        "id": "torrent_5",
        "content_id": "tt10869796",
        "info_hash": "e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6",
        "title": "Leo.2023.Tamil.1080p.BluRay.x264",
        "size": 4294967296,
        "size_readable": "4.0 GB",
        "quality": "1080p",
        "seeders": 250,
        "leechers": 40,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6&dn=Leo.2023.Tamil.1080p.BluRay.x264"
    },
    {
        "id": "torrent_6",
        "content_id": "tt27524176",
        "info_hash": "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1",
        "title": "GOAT.2024.Tamil.1080p.WEB-DL.x264",
        "size": 3500000000,
        "size_readable": "3.3 GB",
        "quality": "1080p",
        "seeders": 300,
        "leechers": 50,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1&dn=GOAT.2024.Tamil.1080p.WEB-DL.x264"
    },
    {
        "id": "torrent_7",
        "content_id": "tt15744286",
        "info_hash": "1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b",
        "title": "Suzhal.The.Vortex.S01.Complete.Tamil.1080p.AMZN.WEB-DL",
        "size": 5000000000,
        "size_readable": "4.7 GB",
        "quality": "1080p",
        "seeders": 120,
        "leechers": 15,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b&dn=Suzhal.The.Vortex.S01.Complete.Tamil.1080p.AMZN.WEB-DL"
    },
    {
        "id": "torrent_8",
        "content_id": "tt21245112",
        "info_hash": "2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c",
        "title": "The.Night.Manager.S01.Complete.Tamil.1080p.DSNP.WEB-DL",
        "size": 6000000000,
        "size_readable": "5.6 GB",
        "quality": "1080p",
        "seeders": 180,
        "leechers": 25,
        "source": "TamilMV",
        "magnet": "magnet:?xt=urn:btih:2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c&dn=The.Night.Manager.S01.Complete.Tamil.1080p.DSNP.WEB-DL"
    },
    {
        "id": "torrent_9",
        "content_id": "tt11427016",
        "info_hash": "3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d",
        "title": "November.Story.S01.Complete.Tamil.1080p.DSNP.WEB-DL",
        "size": 4500000000,
        "size_readable": "4.2 GB",
        "quality": "1080p",
        "seeders": 90,
        "leechers": 12,
        "source": "TamilBlasters",
        "magnet": "magnet:?xt=urn:btih:3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d&dn=November.Story.S01.Complete.Tamil.1080p.DSNP.WEB-DL"
    }
]


def initialize_sample_data():
    content = load_content()
    if not content:
        save_content(SAMPLE_TAMIL_MOVIES + SAMPLE_TAMIL_SERIES)
    
    torrents = load_torrents()
    if not torrents:
        save_torrents(SAMPLE_TORRENTS)


def get_all_content(content_type: Optional[str] = None) -> List[Dict[str, Any]]:
    content = load_content()
    if content_type:
        return [c for c in content if c.get("type") == content_type]
    return content


def get_content_by_id(content_id: str) -> Optional[Dict[str, Any]]:
    content = load_content()
    for c in content:
        if c.get("id") == content_id or c.get("imdb_id") == content_id:
            return c
    return None


def get_torrents_for_content(content_id: str) -> List[Dict[str, Any]]:
    torrents = load_torrents()
    matching = [t for t in torrents if t.get("content_id") == content_id]
    
    if not matching:
        content = get_content_by_id(content_id)
        if content:
            imdb_id = content.get("imdb_id")
            internal_id = content.get("id")
            for t in torrents:
                if t.get("content_id") in [imdb_id, internal_id]:
                    matching.append(t)
    
    return matching


def add_content(content: Dict[str, Any]) -> bool:
    all_content = load_content()
    for i, c in enumerate(all_content):
        if c.get("id") == content.get("id"):
            all_content[i] = content
            save_content(all_content)
            return True
    all_content.append(content)
    save_content(all_content)
    return True


def add_torrent(torrent: Dict[str, Any]) -> bool:
    all_torrents = load_torrents()
    for i, t in enumerate(all_torrents):
        if t.get("info_hash") == torrent.get("info_hash"):
            all_torrents[i] = torrent
            save_torrents(all_torrents)
            return True
    all_torrents.append(torrent)
    save_torrents(all_torrents)
    return True


def search_content(query: str) -> List[Dict[str, Any]]:
    content = load_content()
    query_lower = query.lower()
    return [c for c in content if query_lower in c.get("title", "").lower()]
