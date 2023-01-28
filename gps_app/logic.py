import datetime
from typing import Union, Type, List, Optional, Dict

from .cache import CacheManager
from .models import DeviceGPSInfoTable

class DeviceGPSInfo:
    def __init__(
        self,
        device_id: int,
        latitude: float,
        longitude: float,
        timestamp: datetime.datetime,
        sts: datetime.datetime,
        speed: float,
        id: Optional[int] = None
    ) -> None:
        self.device_id = device_id
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.sts = sts
        self.speed = speed
        self.id = id

    def dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp,
            "sts": self.sts,
            "speed": self.speed,
            "id": self.id
        }

    def _get_cache_value(self) -> dict:
        '''Returns dict which can be used as value for saving in cache.'''
        data_dict = self.dict()
        del data_dict["device_id"]
        return data_dict

    @classmethod
    async def get_from_cache(cls: "Type[DeviceGPSInfo]", device_id: int) -> Union["DeviceGPSInfo", None]:
        value = await CacheManager().get(device_id)
        if value is not None:
            return cls(device_id=device_id, **value)
        return value

    async def set_to_cache(self) -> None:
        existing_instance = await DeviceGPSInfo.get_from_cache(device_id=self.device_id)
        if existing_instance is None or (existing_instance.timestamp < self.timestamp):
            await CacheManager().set(key=self.device_id, value=self._get_cache_value())

    async def _save(self) -> "DeviceGPSInfo":
        '''Saves to db but atomicity is not gauranteed.'''
        gps_dict = self.dict()
        del gps_dict["id"]
        orm_instance = await DeviceGPSInfoTable.create(**gps_dict)
        self.id = orm_instance.id
        return self

    async def save(self, cache=True) -> None:
        '''Saves instance to db. If cache==True, saves in cache too along with db.'''
        gps_dict = self.dict()
        del gps_dict["id"]
        orm_instance = await DeviceGPSInfoTable.create(**gps_dict)
        self.id=orm_instance.id
        if cache:
            await self.set_to_cache()

    @classmethod
    async def filter(cls: Type["DeviceGPSInfo"], **kwargs) -> List["dict"]:
        return await DeviceGPSInfoTable.filter(**kwargs).values(
            id="id",
            device_id="device_id",
            latitude="latitude",
            longitude="longitude",
            timestamp="timestamp",
            sts="sts",
            speed="speed",
        )


class DeviceLocationManager:
    '''This Class provides gateway to interact with DeviceGPSInfo class.'''

    @staticmethod
    async def get_start_and_end_location(
        device_id: int,
    ) -> List[Union[dict, None]]:

        start_location = await DeviceGPSInfoTable.filter(
            device_id=device_id
        ).order_by('timestamp').limit(1).values(
            id="id",
            device_id="device_id",
            latitude="latitude",
            longitude="longitude",
            timestamp="timestamp",
            sts="sts",
            speed="speed",
        )
        end_location = await DeviceGPSInfoTable.filter(
            device_id=device_id
        ).order_by('-timestamp').limit(1).values(
            id="id",
            device_id="device_id",
            latitude="latitude",
            longitude="longitude",
            timestamp="timestamp",
            sts="sts",
            speed="speed",
        )

        ans = [None, None]
        if len(start_location) == 1:
            ans[0] = start_location[0]
        if len(end_location) == 1:
            ans[1] = end_location[0]
        return ans

    @staticmethod
    async def get_from_cache(device_id: int) -> dict:
        return await CacheManager().get(key=device_id)

    @staticmethod
    async def set_to_cache(device_id: int, value: dict):
        return await CacheManager().set(key=device_id, value=value)

    @staticmethod
    async def save_location(location_data: dict):
        return await DeviceGPSInfo.save(DeviceGPSInfo(**location_data))

    @staticmethod
    async def get_all_locations_of_device_between_timestamps(
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        device_id: int
    ) -> List[dict]:
        return await DeviceGPSInfo.filter(
            device_id=device_id, timestamp__gte=start_time, timestamp__lte=end_time)

    @staticmethod
    async def get_all_data_from_cache()->Dict[int, dict]:
        return await CacheManager().get_all()