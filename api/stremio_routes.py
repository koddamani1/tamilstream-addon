from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional, List
import base64
import json
import logging
from api.config import settings
from api.models import UserConfig
from api.content_store import (
    get_all_content, get_content_by_id, get_torrents_for_content,
    search_content, initialize_sample_data, update_content_poster
)
from api.torbox_service import create_torbox_service
from api.metadata_service import get_poster_for_imdb_sync

logger = logging.getLogger(__name__)
router = APIRouter()


def decode_user_config(config_str: Optional[str]) -> UserConfig:
    if not config_str:
        return UserConfig()
    try:
        padding = 4 - len(config_str) % 4
        if padding != 4:
            config_str += '=' * padding
        decoded = base64.urlsafe_b64decode(config_str.encode()).decode()
        config_data = json.loads(decoded)
        return UserConfig(**config_data)
    except Exception as e:
        logger.debug(f"Failed to decode config: {e}")
        return UserConfig()


def encode_user_config(config: UserConfig) -> str:
    config_json = json.dumps(config.model_dump())
    return base64.urlsafe_b64encode(config_json.encode()).decode().rstrip('=')


def get_manifest(config: Optional[str] = None) -> dict:
    return {
        "id": "com.tamilstream.addon",
        "version": settings.app_version,
        "name": settings.app_name,
        "description": settings.app_description,
        "logo": "https://i.imgur.com/Xvy5S5Z.png",
        "background": "https://i.imgur.com/8GtHvBT.jpg",
        "resources": ["catalog", "stream", "meta"],
        "types": ["movie", "series"],
        "catalogs": [
            {
                "id": "tamilstream_movies",
                "type": "movie",
                "name": "Tamil Movies",
                "extra": [
                    {"name": "search", "isRequired": False},
                    {"name": "skip", "isRequired": False}
                ]
            },
            {
                "id": "tamilstream_series",
                "type": "series",
                "name": "Tamil Series",
                "extra": [
                    {"name": "search", "isRequired": False},
                    {"name": "skip", "isRequired": False}
                ]
            }
        ],
        "idPrefixes": ["tt"],
        "behaviorHints": {
            "configurable": True,
            "configurationRequired": False
        }
    }


@router.get("/manifest.json")
async def manifest_root():
    return JSONResponse(
        content=get_manifest(),
        headers={"Access-Control-Allow-Origin": "*"}
    )


@router.get("/{config}/manifest.json")
async def manifest_with_config(config: str):
    return JSONResponse(
        content=get_manifest(config),
        headers={"Access-Control-Allow-Origin": "*"}
    )


@router.get("/catalog/{type}/{id}.json")
async def catalog_root(type: str, id: str, skip: int = 0, search: Optional[str] = None):
    return await handle_catalog(type, id, None, skip, search)


@router.get("/{config}/catalog/{type}/{id}.json")
async def catalog_with_config(config: str, type: str, id: str, skip: int = 0, search: Optional[str] = None):
    return await handle_catalog(type, id, config, skip, search)


async def handle_catalog(type: str, id: str, config: Optional[str], skip: int, search: Optional[str]):
    initialize_sample_data()
    
    if search:
        content_list = search_content(search)
        content_list = [c for c in content_list if c.get("type") == type]
    else:
        content_list = get_all_content(type)
    
    content_list = content_list[skip:skip + 100]
    
    metas = []
    for content in content_list:
        imdb_id = content.get("imdb_id") or content.get("id")
        poster = content.get("poster")
        
        if not poster and imdb_id and imdb_id.startswith("tt"):
            poster = get_poster_for_imdb_sync(imdb_id)
            if poster:
                update_content_poster(imdb_id, poster)
        
        meta = {
            "id": imdb_id,
            "type": content.get("type"),
            "name": content.get("title"),
            "poster": poster,
            "background": content.get("background") or poster,
            "description": content.get("description", ""),
            "releaseInfo": str(content.get("year", "")),
            "imdbRating": str(content.get("rating", "")) if content.get("rating") else None,
            "genres": content.get("genres", []),
            "runtime": content.get("runtime")
        }
        metas.append(meta)
    
    return JSONResponse(
        content={"metas": metas},
        headers={"Access-Control-Allow-Origin": "*"}
    )


@router.get("/meta/{type}/{id}.json")
async def meta_root(type: str, id: str):
    return await handle_meta(type, id, None)


@router.get("/{config}/meta/{type}/{id}.json")
async def meta_with_config(config: str, type: str, id: str):
    return await handle_meta(type, id, config)


async def handle_meta(type: str, id: str, config: Optional[str]):
    initialize_sample_data()
    
    content_id = id.replace(".json", "")
    content = get_content_by_id(content_id)
    
    if not content:
        return JSONResponse(
            content={"meta": None},
            headers={"Access-Control-Allow-Origin": "*"}
        )
    
    imdb_id = content.get("imdb_id") or content.get("id")
    poster = content.get("poster")
    
    if not poster and imdb_id and imdb_id.startswith("tt"):
        poster = get_poster_for_imdb_sync(imdb_id)
        if poster:
            update_content_poster(imdb_id, poster)
    
    meta_data = {
        "id": imdb_id,
        "type": content.get("type"),
        "name": content.get("title"),
        "poster": poster,
        "background": content.get("background") or poster,
        "description": content.get("description", ""),
        "releaseInfo": str(content.get("year", "")),
        "imdbRating": str(content.get("rating", "")) if content.get("rating") else None,
        "genres": content.get("genres", []),
        "runtime": content.get("runtime")
    }
    
    if content.get("type") == "series" and content.get("videos"):
        meta_data["videos"] = content.get("videos", [])
    
    return JSONResponse(
        content={"meta": meta_data},
        headers={"Access-Control-Allow-Origin": "*"}
    )


@router.get("/stream/{type}/{id}.json")
async def stream_root(type: str, id: str):
    return await handle_stream(type, id, None)


@router.get("/{config}/stream/{type}/{id}.json")
async def stream_with_config(config: str, type: str, id: str):
    return await handle_stream(type, id, config)


async def handle_stream(type: str, id: str, config: Optional[str]):
    initialize_sample_data()
    user_config = decode_user_config(config)
    
    raw_id = id.replace(".json", "")
    
    episode_info = None
    base_content_id = raw_id
    
    if ":" in raw_id:
        parts = raw_id.split(":")
        base_content_id = parts[0]
        if len(parts) >= 3:
            try:
                episode_info = {"season": int(parts[1]), "episode": int(parts[2])}
            except ValueError:
                pass
    
    torrents = get_torrents_for_content(base_content_id)
    
    if not torrents:
        content = get_content_by_id(base_content_id)
        if content:
            lookup_id = content.get("imdb_id") or content.get("id")
            if lookup_id != base_content_id:
                torrents = get_torrents_for_content(lookup_id)
    
    if not torrents:
        return JSONResponse(
            content={"streams": []},
            headers={"Access-Control-Allow-Origin": "*"}
        )
    
    streams = []
    torbox_service = None
    
    if user_config.torbox_api_key:
        torbox_service = create_torbox_service(user_config.torbox_api_key)
    
    for torrent in torrents:
        info_hash = torrent.get("info_hash")
        magnet = torrent.get("magnet")
        quality = torrent.get("quality", "Unknown")
        size = torrent.get("size_readable", "")
        seeders = torrent.get("seeders", 0)
        source = torrent.get("source", "Unknown")
        torrent_title = torrent.get("title", "")
        
        if not info_hash:
            continue
        
        title_parts = [
            f"TamilStream | {quality}",
            f"{size} | {seeders} seeders",
            f"Source: {source}"
        ]
        
        stream_data = {
            "name": settings.app_name,
            "title": "\n".join(title_parts),
            "infoHash": info_hash,
            "behaviorHints": {
                "bingeGroup": f"tamilstream-{quality}",
                "notWebReady": True
            }
        }
        
        torbox_success = False
        if torbox_service and user_config.torbox_api_key and magnet:
            try:
                is_cached = await torbox_service.check_cache(info_hash)
                
                if is_cached:
                    result = await torbox_service.add_magnet(magnet, torrent_title)
                    
                    if result:
                        torrent_id = result.get("torrent_id") or result.get("id")
                        
                        if torrent_id:
                            torrent_info = await torbox_service.get_torrent_info(str(torrent_id))
                            
                            file_id = None
                            if torrent_info and torrent_info.get("files"):
                                files = torrent_info["files"]
                                video_files = [f for f in files if any(
                                    f.get("name", "").lower().endswith(ext) 
                                    for ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv']
                                )]
                                
                                if video_files:
                                    if episode_info:
                                        ep_num = episode_info["episode"]
                                        for vf in video_files:
                                            if f"e{ep_num:02d}" in vf.get("name", "").lower() or \
                                               f"episode{ep_num}" in vf.get("name", "").lower() or \
                                               f"ep{ep_num}" in vf.get("name", "").lower():
                                                file_id = vf.get("id")
                                                break
                                    
                                    if not file_id:
                                        largest_file = max(video_files, key=lambda f: f.get("size", 0))
                                        file_id = largest_file.get("id")
                            
                            download_url = await torbox_service.get_download_link(
                                str(torrent_id), 
                                str(file_id) if file_id else None
                            )
                            
                            if download_url:
                                stream_data = {
                                    "name": settings.app_name,
                                    "title": f"[CACHED] {title_parts[0]}\n{title_parts[1]}\n{title_parts[2]}",
                                    "url": download_url,
                                    "behaviorHints": {
                                        "bingeGroup": f"tamilstream-{quality}",
                                        "notWebReady": False
                                    }
                                }
                                torbox_success = True
                    
                    if not torbox_success and is_cached:
                        stream_data["title"] = f"[CACHED] {stream_data['title']}"
                        
            except Exception as e:
                logger.error(f"TorBox error for {info_hash}: {e}")
        
        streams.append(stream_data)
    
    streams.sort(key=lambda x: (
        0 if x.get("url") else 1,
        0 if "[CACHED]" in x.get("title", "") else 1,
        -1 if "4K" in x.get("title", "") else 
        0 if "1080p" in x.get("title", "") else 
        1 if "HD" in x.get("title", "") else 2
    ))
    
    return JSONResponse(
        content={"streams": streams},
        headers={"Access-Control-Allow-Origin": "*"}
    )
