import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv("ENV")

def get_api_url():
    if ENV == "dev":
        return os.getenv("DEV_API_URL")
    elif ENV == "prod":
        return os.getenv("API_URL")
