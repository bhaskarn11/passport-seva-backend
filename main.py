from fastapi import FastAPI
from settings import get_settings

config = get_settings()

app = FastAPI(version=config.version, title=config.app_name)


@app.get("/")
def home():
    return {"hello": "world"}
