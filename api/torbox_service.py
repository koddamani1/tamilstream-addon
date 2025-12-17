import httpx
from typing import Optional, Dict, Any, List
from api.config import settings
import logging

logger = logging.getLogger(__name__)


class TorBoxService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = settings.torbox_api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def verify_api_key(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/user/me",
                    headers=self.headers,
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error verifying TorBox API key: {e}")
            return False
    
    async def get_user_info(self) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/user/me",
                    headers=self.headers,
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json().get("data")
                return None
        except Exception as e:
            logger.error(f"Error getting TorBox user info: {e}")
            return None
    
    async def add_magnet(self, magnet: str, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            data = {"magnet": magnet}
            if name:
                data["name"] = name
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/torrents/createtorrent",
                    headers=self.headers,
                    json=data,
                    timeout=30.0
                )
                if response.status_code == 200:
                    return response.json().get("data")
                logger.error(f"TorBox add magnet error: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error adding magnet to TorBox: {e}")
            return None
    
    async def get_torrent_list(self) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/torrents/mylist",
                    headers=self.headers,
                    timeout=15.0
                )
                if response.status_code == 200:
                    return response.json().get("data", [])
                return []
        except Exception as e:
            logger.error(f"Error getting TorBox torrent list: {e}")
            return []
    
    async def get_torrent_info(self, torrent_id: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/torrents/mylist",
                    headers=self.headers,
                    params={"id": torrent_id},
                    timeout=15.0
                )
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    if data:
                        return data[0] if isinstance(data, list) else data
                return None
        except Exception as e:
            logger.error(f"Error getting TorBox torrent info: {e}")
            return None
    
    async def get_download_link(self, torrent_id: str, file_id: Optional[str] = None) -> Optional[str]:
        try:
            params = {"token": self.api_key, "torrent_id": torrent_id}
            if file_id:
                params["file_id"] = file_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/torrents/requestdl",
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                if response.status_code == 200:
                    return response.json().get("data")
                logger.error(f"TorBox download link error: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting TorBox download link: {e}")
            return None
    
    async def check_cache(self, info_hash: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/torrents/checkcached",
                    headers=self.headers,
                    params={"hash": info_hash},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json().get("data", {})
                    return data.get(info_hash, False)
                return False
        except Exception as e:
            logger.error(f"Error checking TorBox cache: {e}")
            return False
    
    async def delete_torrent(self, torrent_id: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/torrents/controltorrent",
                    headers=self.headers,
                    json={"torrent_id": torrent_id, "operation": "delete"},
                    timeout=15.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error deleting TorBox torrent: {e}")
            return False


def create_torbox_service(api_key: str) -> TorBoxService:
    return TorBoxService(api_key)
