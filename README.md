# api.tahm-ken.ch

## dev setup

requirements:
- docker or redis
- python

```bash
# start a redis server
docker compose -f compose-dev.yaml up -d

# create a venv and download requirements
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# create config file
cp .env_sample .env
vim .env # set your Riot API key

# start dev server
fastapi dev
```