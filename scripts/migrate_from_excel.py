import pandas as pd, os
from tortoise import Tortoise, run_async

from gps_app.logic import DeviceLocationManager
from gps_app.config import DBURL

csv_file = "./static/raw_data.csv"

async def connect_to_db()->None:
    await Tortoise.init(
        db_url=DBURL,
        modules={"models": ["gps_app.models"]}
    )

async def save_to_db(csv_file=csv_file):
    df = pd.read_csv(csv_file)
    df.sort_values('sts')
    for _, row in df.iterrows():
        data = {}
        data["device_id"]=row["device_fk_id"]
        data["latitude"]=row["latitude"]
        data["longitude"]=row["longitude"]
        data["timestamp"]=row["time_stamp"]
        data["sts"]=row["sts"]
        data["speed"]=row["speed"]
        await connect_to_db()
        await DeviceLocationManager.save_location(location_data=data)

def save_data_to_db_and_cache():
    run_async(save_to_db())