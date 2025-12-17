"""
Database models and connection for TamilStream addon
"""

import os
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = None
SessionLocal = None
Base = None
Content = None
Torrent = None
Episode = None
_sqlalchemy_available = False

try:
    from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    _sqlalchemy_available = True
    Base = declarative_base()
    
    class _Content(Base):
        __tablename__ = "content"
        
        id = Column(String, primary_key=True)
        imdb_id = Column(String, index=True, nullable=True)
        title = Column(String, nullable=False)
        type = Column(String, default="series")
        poster = Column(String, nullable=True)
        background = Column(String, nullable=True)
        description = Column(Text, nullable=True)
        year = Column(Integer, nullable=True)
        rating = Column(String, nullable=True)
        genres = Column(JSON, default=list)
        runtime = Column(String, nullable=True)
        channel = Column(String, nullable=True)
        source_url = Column(String, nullable=True)
        videos = Column(JSON, default=list)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class _Torrent(Base):
        __tablename__ = "torrents"
        
        id = Column(String, primary_key=True)
        content_id = Column(String, index=True, nullable=False)
        info_hash = Column(String, unique=True, nullable=False)
        title = Column(String, nullable=False)
        size = Column(Integer, default=0)
        size_readable = Column(String, nullable=True)
        quality = Column(String, nullable=True)
        seeders = Column(Integer, default=0)
        leechers = Column(Integer, default=0)
        source = Column(String, nullable=True)
        magnet = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow)

    class _Episode(Base):
        __tablename__ = "episodes"
        
        id = Column(String, primary_key=True)
        content_id = Column(String, index=True, nullable=False)
        title = Column(String, nullable=False)
        season = Column(Integer, default=1)
        episode = Column(Integer, nullable=True)
        episode_date = Column(String, nullable=True)
        source_url = Column(String, nullable=True)
        poster = Column(String, nullable=True)
        video_sources = Column(JSON, default=list)
        created_at = Column(DateTime, default=datetime.utcnow)
    
    Content = _Content
    Torrent = _Torrent
    Episode = _Episode

except ImportError:
    _sqlalchemy_available = False


def init_db():
    """Initialize database connection and create tables"""
    global engine, SessionLocal
    
    if not _sqlalchemy_available or not DATABASE_URL:
        return False
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False


def get_db():
    """Get database session"""
    if not _sqlalchemy_available:
        return None
    if SessionLocal is None:
        if not init_db():
            return None
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        return db
    except:
        db.close()
        return None
