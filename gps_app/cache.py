import aioredis, json
from typing import Union, Any

from .config import redis_url

class CacheManager:
    _redis_url = redis_url

    def __init__(self)->None:
        self.cache_instance = aioredis.from_url(self._redis_url, decode_responses=True)

    async def set(self, key: Union[int, str], value: Any)->None:
        return await self.cache_instance.set(name=key, value=json.dumps(value))

    async def get(self, key: Union[int, str])->Any:
        '''Returns None if key not found.'''
        value = await self.cache_instance.get(name=key)
        return json.loads(value) if value is not None else value

    async def get_all(self)->Any:
        all_keys = await self.cache_instance.keys()
        return {key : await self.get(key) for key in all_keys}