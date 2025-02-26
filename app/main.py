from fastapi import FastAPI, Request
from riot_api import query
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()
limiter = Limiter(key_func=get_remote_address, storage_uri=f"redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/n")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def root():
    return {"version": os.getenv("VERSION")}

@app.get("/player_data/{region}/{gameNamesTags}")
@limiter.limit("15/minute")
def player_data(request: Request, region:str, gameNamesTags: str, masteries: bool = False):
    accounts = []
    gameNamesParsed = [tuple(gameNameTag.split("-")) for gameNameTag in set(gameNamesTags.split(","))]

    if len(gameNamesParsed) > 7:
        return accounts

    for gameNameTag in gameNamesParsed:
        if len(gameNameTag) != 2:
           continue
        
        gameName, tagLine = gameNameTag
        try:
            data = {}
            data["account"] = account_by_riot_id(gameName, tagLine)
            puuid = data["account"]["puuid"]
            data["challenges"] = challenges_player_data(puuid, region)
            data["summoner"] = summoner(puuid, region)
            if masteries:
                data["champion_masteries"] = champion_masteries(puuid, region)
            accounts.append(data)
        except Exception as e:
            print(e)
            pass
    return accounts

def account_by_riot_id(gameName, tagLine):
    return query(f"/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}")

def champion_masteries(puuid, region):
    return query(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}", region, expire=86400)

def challenges_player_data(puuid, region):
    return query(f"/lol/challenges/v1/player-data/{puuid}", region, expire=10)

def summoner(puuid, region):
    return query(f"/lol/summoner/v4/summoners/by-puuid/{puuid}", region, expire=86400)