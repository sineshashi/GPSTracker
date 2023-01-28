from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException
import datetime

from .logic import DeviceLocationManager
from .datatypes import LatestDataReturnType, StartAndEndReturnType, AllDataReturnType

router = APIRouter()

@router.get("/getLatestPosition", response_model=LatestDataReturnType)
async def get_latest_position(deviceID: int):
    '''Returns latest data recorded for the given deviceID.'''
    res = await DeviceLocationManager.get_from_cache(device_id=deviceID)
    if res is None:
        raise HTTPException(status_code=404, detail="DeviceID does not exist,")
    print(res)
    return res

@router.get("/getStartAndEndLocationOfDevice", response_model=StartAndEndReturnType)
async def get_start_and_end_location_of_device(deviceID: int):
    '''Returns start and end location in [lat, long] type tuples.'''
    start_data, end_data = await DeviceLocationManager.get_start_and_end_location(device_id=deviceID)
    returning_data = {"start_location": [], "end_location": []}
    if start_data is not None:
        returning_data["start_location"]=[start_data["latitude"], start_data["longitude"]]
    if end_data is not None:
        returning_data["end_location"]=[end_data["latitude"], end_data["longitude"]]
    return returning_data

@router.post("/listAllLocationVisitedBetween", response_model=AllDataReturnType)
async def list_all_locations_visited_between_given_time(
    deviceID:int=Body(embed=True),
    start_time: datetime.datetime=Body(embed=True),
    end_time: datetime.datetime=Body(embed=True)
):
    all_locations = await DeviceLocationManager.get_all_locations_of_device_between_timestamps(
        start_time=start_time,
        end_time=end_time,
        device_id=deviceID
    )
    return {"all_locations": all_locations}