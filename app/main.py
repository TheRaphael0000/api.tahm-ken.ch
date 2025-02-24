from fastapi import FastAPI
from riot_api import query
import os

app = FastAPI()

@app.get("/")
def root():
    return {"version": os.getenv("VERSION")}

@app.get("/challenges_player_data/{region}/{gameNamesTags}")
def account_by_riot_id_dev(region:str, gameNamesTags: str, masteries: bool = False):
    accounts = []
    gameNamesParsed = [gameNameTag.split("-") for gameNameTag in gameNamesTags.split(",")]

    print(masteries)
    for gameName, tagLine in gameNamesParsed:
        try:
            data = {}
            data["account"] = account_by_riot_id(gameName, tagLine)
            puuid = data["account"]["puuid"]
            data["challenges"] = challenges = challenges_player_data(puuid, region)
            if masteries:
                data["champion_masteries"] = champion_masteries(puuid, region)
            accounts.append(data)
        except:
            pass
    return accounts

def account_by_riot_id(gameName, tagLine):
    return query(f"/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}")

def champion_masteries(puuid, region):
    return query(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}", region, expire=86400)

def challenges_player_data(puuid, region):
    return query(f"/lol/challenges/v1/player-data/{puuid}", region, expire=10)