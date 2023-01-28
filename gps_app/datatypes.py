from typing import List
import datetime
from pydantic import BaseModel, Extra

class LatestDataReturnType(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime.datetime
    sts: datetime.datetime
    speed: float

class StartAndEndReturnType(BaseModel):
    start_location: List[float]
    end_location: List[float]

class LocationDataType(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime.datetime

    class Config:
        extra=Extra.ignore

class AllDataReturnType(BaseModel):
    all_locations: List[LocationDataType]
    
    class Config:
        extra=Extra.ignore