import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Explicitly load .env file
load_dotenv(override=True)

app = FastAPI()

@app.get("/get_info")
def get_info():
    app_version = os.getenv("APP_VERSION", "default_version")
    app_title = os.getenv("APP_TITLE", "default_title")
    return {"app_version": app_version, "app_title": app_title}
