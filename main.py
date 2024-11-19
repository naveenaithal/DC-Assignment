import os
from fastapi import FastAPI
from dotenv import load_dotenv
from prometheus_fastapi_instrumentator import Instrumentator

# Explicitly load .env file
load_dotenv(override=True)

# Create the FastAPI application
app = FastAPI()
Instrumentator().instrument(app).expose(app)


@app.get("/get_info")
def get_info():
    app_version = os.getenv("APP_VERSION", "default_version")
    app_title = os.getenv("APP_TITLE", "default_title")
    user_name = os.getenv("USER_NAME", "bits")
    register_number = os.getenv("REGISTER_NUMBER", "999")
    description = os.getenv("APP_DESCRIPTION", "default description")
    return {"app_version": app_version, "app_title": app_title,"user_name":user_name,"register_number":register_number,"description":description}


