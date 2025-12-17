"""
Content store with PostgreSQL database storage
"""

from typing import Optional, List, Dict, Any
import json
import os
import logging
from datetime import datetime

from api.db import init_db, get_db, Content, Torrent, Episode

logger = logging.getLogger(__name__)

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
            {"id": "tt15744286:1:4", "title": "Episode 4", "season": 1, "episode": 4},
            {"id": "tt15744286:1:5", "title": "Episode 5", "season": 1, "episode": 5},
            {"id": "tt15744286:1:6", "title": "Episode 6", "season": 1, "episode": 6},
            {"id": "tt15744286:1:7", "title": "Episode 7", "season": 1, "episode": 7},
            {"id": "tt15744286:1:8", "title": "Episode 8", "season": 1, "episode": 8}
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
            {"id": "tt21245112:1:3", "title": "Episode 3", "season": 1, "episode": 3},
            {"id": "tt21245112:1:4", "title": "Episode 4", "season": 1, "episode": 4},
            {"id": "tt21245112:1:5", "title": "Episode 5", "season": 1, "episode": 5},
            {"id": "tt21245112:1:6", "title": "Episode 6", "season": 1, "episode": 6},
            {"id": "tt21245112:1:7", "title": "Episode 7", "season": 1, "episode": 7}
        ]
    },
    {
        "id": "tt11427016",
        "imdb_id": "tt11427016",
        "title": "November Story",
        "year": 2021,
        "type": "series",
        "description": "A young woman fights to prove her father's innocence in a murder case.",
        "genres": ["Crime", "Mystery", "Thriller"],
        "rating": 8.0,
        "runtime": "45 min",
        "videos": [
            {"id": "tt11427016:1:1", "title": "Episode 1", "season": 1, "episode": 1},
            {"id": "tt11427016:1:2", "title": "Episode 2", "season": 1, "episode": 2},
            {"id": "tt11427016:1:3", "title": "Episode 3", "season": 1, "episode": 3},
            {"id": "tt11427016:1:4", "title": "Episode 4", "season": 1, "episode": 4},
            {"id": "tt11427016:1:5", "title": "Episode 5", "season": 1, "episode": 5},
            {"id": "tt11427016:1:6", "title": "Episode 6", "season": 1, "episode": 6},
            {"id": "tt11427016:1:7", "title": "Episode 7", "season": 1, "episode": 7}
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
        "magnet": "magnet:?xt=urn:btih:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2&dn=Ponniyin.Selvan.I.2022.Tamil.1080p.BluRay.x264"
    },
    {
        "id": "torrent_2",
        "content_id": "tt21064584",
        "info_hash": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        "title": "Jailer.2023.Tamil.1080p.WEB-DL.x264",
        "size": 3221225472,
        "size_readable": "3.0 GB",
        "quality": "1080p",
        "seeders": 200,
        "leechers": 30,
        "source": "TamilBlasters",
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

_db_initialized = False


def _content_to_dict(content: Content) -> Dict[str, Any]:
    """Convert Content model to dictionary"""
    return {
        "id": content.id,
        "imdb_id": content.imdb_id,
        "title": content.title,
        "type": content.type,
        "poster": content.poster,
        "background": content.background,
        "description": content.description,
        "year": content.year,
        "rating": content.rating,
        "genres": content.genres or [],
        "runtime": content.runtime,
        "channel": content.channel,
        "source_url": content.source_url,
        "videos": content.videos or []
    }


def _torrent_to_dict(torrent: Torrent) -> Dict[str, Any]:
    """Convert Torrent model to dictionary"""
    return {
        "id": torrent.id,
        "content_id": torrent.content_id,
        "info_hash": torrent.info_hash,
        "title": torrent.title,
        "size": torrent.size,
        "size_readable": torrent.size_readable,
        "quality": torrent.quality,
        "seeders": torrent.seeders,
        "leechers": torrent.leechers,
        "source": torrent.source,
        "magnet": torrent.magnet
    }


def initialize_sample_data():
    """Initialize database with sample data if empty"""
    global _db_initialized
    
    if _db_initialized:
        return
    
    if not init_db():
        logger.warning("Database not available, using sample data only")
        _db_initialized = True
        return
    
    db = get_db()
    if not db:
        _db_initialized = True
        return
    
    try:
        existing = db.query(Content).count()
        if existing == 0:
            for movie in SAMPLE_TAMIL_MOVIES:
                content = Content(
                    id=movie["id"],
                    imdb_id=movie.get("imdb_id"),
                    title=movie["title"],
                    type=movie.get("type", "movie"),
                    description=movie.get("description"),
                    year=movie.get("year"),
                    rating=str(movie.get("rating")) if movie.get("rating") else None,
                    genres=movie.get("genres", []),
                    runtime=movie.get("runtime")
                )
                db.merge(content)
            
            for series in SAMPLE_TAMIL_SERIES:
                content = Content(
                    id=series["id"],
                    imdb_id=series.get("imdb_id"),
                    title=series["title"],
                    type="series",
                    description=series.get("description"),
                    year=series.get("year"),
                    rating=str(series.get("rating")) if series.get("rating") else None,
                    genres=series.get("genres", []),
                    runtime=series.get("runtime"),
                    videos=series.get("videos", [])
                )
                db.merge(content)
            
            db.commit()
            logger.info("Initialized database with sample content")
        
        existing_torrents = db.query(Torrent).count()
        if existing_torrents == 0:
            for t in SAMPLE_TORRENTS:
                torrent = Torrent(
                    id=t["id"],
                    content_id=t["content_id"],
                    info_hash=t["info_hash"],
                    title=t["title"],
                    size=t.get("size", 0),
                    size_readable=t.get("size_readable"),
                    quality=t.get("quality"),
                    seeders=t.get("seeders", 0),
                    leechers=t.get("leechers", 0),
                    source=t.get("source"),
                    magnet=t.get("magnet")
                )
                db.merge(torrent)
            
            db.commit()
            logger.info("Initialized database with sample torrents")
        
        _db_initialized = True
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()


def get_all_content(content_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all content from database"""
    db = get_db()
    if not db:
        if content_type:
            return [c for c in SAMPLE_TAMIL_MOVIES + SAMPLE_TAMIL_SERIES if c.get("type") == content_type]
        return SAMPLE_TAMIL_MOVIES + SAMPLE_TAMIL_SERIES
    
    try:
        if content_type:
            results = db.query(Content).filter(Content.type == content_type).all()
        else:
            results = db.query(Content).all()
        
        return [_content_to_dict(c) for c in results]
    except Exception as e:
        logger.error(f"Error getting content: {e}")
        return []
    finally:
        db.close()


def get_content_by_id(content_id: str) -> Optional[Dict[str, Any]]:
    """Get content by ID"""
    db = get_db()
    if not db:
        for c in SAMPLE_TAMIL_MOVIES + SAMPLE_TAMIL_SERIES:
            if c.get("id") == content_id or c.get("imdb_id") == content_id:
                return c
        return None
    
    try:
        content = db.query(Content).filter(
            (Content.id == content_id) | (Content.imdb_id == content_id)
        ).first()
        
        return _content_to_dict(content) if content else None
    except Exception as e:
        logger.error(f"Error getting content by id: {e}")
        return None
    finally:
        db.close()


def get_torrents_for_content(content_id: str) -> List[Dict[str, Any]]:
    """Get torrents for a specific content"""
    db = get_db()
    if not db:
        matching = [t for t in SAMPLE_TORRENTS if t.get("content_id") == content_id]
        return matching
    
    try:
        content = get_content_by_id(content_id)
        if not content:
            return []
        
        imdb_id = content.get("imdb_id")
        internal_id = content.get("id")
        
        torrents = db.query(Torrent).filter(
            (Torrent.content_id == content_id) |
            (Torrent.content_id == imdb_id) |
            (Torrent.content_id == internal_id)
        ).all()
        
        return [_torrent_to_dict(t) for t in torrents]
    except Exception as e:
        logger.error(f"Error getting torrents: {e}")
        return []
    finally:
        db.close()


def search_content(query: str) -> List[Dict[str, Any]]:
    """Search content by title"""
    db = get_db()
    if not db:
        query_lower = query.lower()
        return [c for c in SAMPLE_TAMIL_MOVIES + SAMPLE_TAMIL_SERIES 
                if query_lower in c.get("title", "").lower()]
    
    try:
        results = db.query(Content).filter(
            Content.title.ilike(f"%{query}%")
        ).all()
        
        return [_content_to_dict(c) for c in results]
    except Exception as e:
        logger.error(f"Error searching content: {e}")
        return []
    finally:
        db.close()


def update_content_poster(content_id: str, poster_url: str) -> bool:
    """Update poster URL for content"""
    db = get_db()
    if not db:
        return False
    
    try:
        content = db.query(Content).filter(
            (Content.id == content_id) | (Content.imdb_id == content_id)
        ).first()
        
        if content:
            content.poster = poster_url
            content.updated_at = datetime.utcnow()
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error updating poster: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def add_content(content_data: Dict[str, Any]) -> bool:
    """Add or update content in database"""
    db = get_db()
    if not db:
        return False
    
    try:
        content = Content(
            id=content_data.get("id"),
            imdb_id=content_data.get("imdb_id"),
            title=content_data.get("title"),
            type=content_data.get("type", "series"),
            poster=content_data.get("poster"),
            background=content_data.get("background"),
            description=content_data.get("description"),
            year=content_data.get("year"),
            rating=str(content_data.get("rating")) if content_data.get("rating") else None,
            genres=content_data.get("genres", []),
            runtime=content_data.get("runtime"),
            channel=content_data.get("channel"),
            source_url=content_data.get("source_url"),
            videos=content_data.get("videos", [])
        )
        db.merge(content)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error adding content: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def add_torrent(torrent_data: Dict[str, Any]) -> bool:
    """Add or update torrent in database"""
    db = get_db()
    if not db:
        return False
    
    try:
        torrent = Torrent(
            id=torrent_data.get("id"),
            content_id=torrent_data.get("content_id"),
            info_hash=torrent_data.get("info_hash"),
            title=torrent_data.get("title"),
            size=torrent_data.get("size", 0),
            size_readable=torrent_data.get("size_readable"),
            quality=torrent_data.get("quality"),
            seeders=torrent_data.get("seeders", 0),
            leechers=torrent_data.get("leechers", 0),
            source=torrent_data.get("source"),
            magnet=torrent_data.get("magnet")
        )
        db.merge(torrent)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error adding torrent: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def add_episode(episode_data: Dict[str, Any]) -> bool:
    """Add or update episode in database"""
    db = get_db()
    if not db:
        return False
    
    try:
        episode = Episode(
            id=episode_data.get("id"),
            content_id=episode_data.get("content_id"),
            title=episode_data.get("title"),
            season=episode_data.get("season", 1),
            episode=episode_data.get("episode"),
            episode_date=episode_data.get("episode_date"),
            source_url=episode_data.get("source_url"),
            poster=episode_data.get("poster"),
            video_sources=episode_data.get("video_sources", [])
        )
        db.merge(episode)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error adding episode: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def get_content_count() -> int:
    """Get total content count in database"""
    db = get_db()
    if not db:
        return len(SAMPLE_TAMIL_MOVIES) + len(SAMPLE_TAMIL_SERIES)
    
    try:
        return db.query(Content).count()
    except Exception as e:
        logger.error(f"Error counting content: {e}")
        return 0
    finally:
        db.close()
