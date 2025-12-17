from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    MOVIE = "movie"
    SERIES = "series"


class StreamQuality(str, Enum):
    CAM = "CAM"
    HDCAM = "HDCAM"
    HDTS = "HDTS"
    HD = "HD"
    FULL_HD = "1080p"
    UHD_4K = "4K"
    UNKNOWN = "Unknown"


class TamilContent(BaseModel):
    id: str
    imdb_id: Optional[str] = None
    title: str
    original_title: Optional[str] = None
    year: Optional[int] = None
    type: ContentType
    poster: Optional[str] = None
    background: Optional[str] = None
    description: Optional[str] = None
    genres: List[str] = []
    rating: Optional[float] = None
    runtime: Optional[str] = None
    
    season: Optional[int] = None
    episode: Optional[int] = None
    episode_title: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TorrentInfo(BaseModel):
    id: str
    content_id: str
    info_hash: str
    title: str
    size: int = 0
    size_readable: str = ""
    quality: StreamQuality = StreamQuality.UNKNOWN
    seeders: int = 0
    leechers: int = 0
    source: str = ""
    magnet: Optional[str] = None
    
    season: Optional[int] = None
    episode: Optional[int] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StremioMeta(BaseModel):
    id: str
    type: str
    name: str
    poster: Optional[str] = None
    background: Optional[str] = None
    description: Optional[str] = None
    releaseInfo: Optional[str] = None
    imdbRating: Optional[str] = None
    genres: List[str] = []
    runtime: Optional[str] = None


class StremioStream(BaseModel):
    url: Optional[str] = None
    infoHash: Optional[str] = None
    title: str
    name: Optional[str] = None
    behaviorHints: Optional[Dict[str, Any]] = None


class StremioCatalog(BaseModel):
    metas: List[StremioMeta]


class StremioManifest(BaseModel):
    id: str
    version: str
    name: str
    description: str
    logo: Optional[str] = None
    background: Optional[str] = None
    resources: List[str]
    types: List[str]
    catalogs: List[Dict[str, Any]]
    idPrefixes: Optional[List[str]] = None
    behaviorHints: Optional[Dict[str, Any]] = None


class UserConfig(BaseModel):
    torbox_api_key: str = ""
    quality_filter: List[str] = ["1080p", "HD", "4K"]
    show_cam_quality: bool = False
