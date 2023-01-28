import sys, subprocess, uvicorn

from gps_app.config import MIGRATION_LOCATION, DEPLOYMENT_DETAILS

if __name__ == "__main__":
    if sys.argv == ["manage.py", "migrate", "first", "time"]:
        subprocess.run(["aerich", "init", "-t", "gps_app.main.db_config", "--location", MIGRATION_LOCATION])
        subprocess.run(["aerich", "init-db"])
    
    if sys.argv == ["manage.py", "migrate"]:
        print("Please give migration a name.")
        migration_name = input()
        commands = [["aerich", "migrate", "--name", migration_name], ["aerich", "upgrade"]]
        for cmd in commands:
            subprocess.run(cmd)

    if sys.argv == ["manage.py", "runserver"]:
        uvicorn.run("gps_app.main:app", port = DEPLOYMENT_DETAILS["PORT"], host=DEPLOYMENT_DETAILS["HOST"], reload=True, lifespan="on")

    if sys.argv == ["manage.py", "populate"]:
        from scripts import migrate_from_excel
        migrate_from_excel.save_data_to_db_and_cache()

    if sys.argv == ["manage.py", "get", "cache"]:
        from scripts import get_data_in_cache
        get_data_in_cache.fetch_cache_data()