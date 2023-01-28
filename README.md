# gps_tracker

This repository contains APIs for getting gps coordinates from the database and has scripts to feed the data.
To get live APIs, please visit https://gps-tracker-or64.onrender.com/docs

The above url for docs will be slow as render is slow for the free services and first hit can take upto few minutes but after that it will be quite fast.

# Steps
    Use Python 3.6 or above. This repository has been built and test with Python 3.7.8.
    1. Create virtual environment by:

            python -m venev env

    2. Activate env by:

            ./env/Scripts/Activate

    3. Install required packages by:
        
            pip install -r requirements.txt

    4.  Can change database and redis configurations from gps_app/config.py file.

# Migration

    To migrate db first time use
        
        python manage.py migrate first time

    For latter migrations use:

        python manage.py migrate

# Population of data

    To feed data using csv file, use:

        python manage.py populate

    This will populate data from existing csv sheet in static folder.

# Fetching Data Saved in Cache

    To get all the data that has been saved in cache, use:

        python manage.py get cache

    This will save all data in json and csv file in static folder.

# About technical information

    This repository uses fastapi to provide restAPIs and tortoise-orm to interact with db saved in postgres.
    To cache, it uses redis and aioredis, an asyncio version of redis, library has been to used to make it faster.

    **gps_app**
        This folder contains all the logic to provide APIs and interacting with redis and postgres. Main files are:
        
        1. models.py file contains tortoise-models which are reponsible to create tables in db and interact with them.
        
        2. logic.py file contains all the functions to interact with db and redis. DeviceLocationManager class provides all the methods for our purpose.

        3. apis.py file has all the routes for restAPIs and their view functions.

        4. main.py file is responsible for starting server and connecting to database.

    **scripts**
        
        This folder provides some scripts like feeding raw data to sql and redis, getting all the data currently saved in redis.