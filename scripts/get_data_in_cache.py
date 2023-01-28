import json, pandas as pd, asyncio, os
from gps_app.logic import DeviceLocationManager

if not os.path.exists("./static"):
    os.makedirs("./static")

target_csv_for_cache_data_saving = "./static/cached_data.csv"
target_json_for_cache_saving = "./static/cached_data.json"

async def get_all_data_saved_in_cache():
    all_data = await DeviceLocationManager.get_all_data_from_cache()
    with open(target_json_for_cache_saving, "w") as file:
        file.write(json.dumps(all_data))
    def _transform(key, value):
        value["device_id"]=key
        return value
    data_arr = [_transform(key, value) for key, value in all_data.items()]
    df = pd.DataFrame(data_arr)
    df.to_csv(target_csv_for_cache_data_saving)

def fetch_cache_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_all_data_saved_in_cache())