import requests
import os
import json
import redis
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

riot_endpoint = "https://europe.api.riotgames.com"
league_endpoint = "https://{0}.api.riotgames.com"

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))

def query(url, region=None, expire=None):
    if region and len(region) > 4:
        raise HTTPException(status_code=400, detail="Region too long")
    
    key = f"{url}-{region}"

    result = r.get(key)
    if result:
        return json.loads(result)
    
    if region is None:
        url = f"{riot_endpoint}{url}"
    else:
        url = f"{league_endpoint}{url}".format(region)

    print(url)
    response = requests.get(
        url, headers={"X-Riot-Token": os.getenv("RIOT_API")})
    data = response.json()

    r.set(key, json.dumps(data))
    if expire:
        r.expire(key, expire)

    return data