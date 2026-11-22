import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OFFER_ID = os.getenv("OFFER_ID")
LAVA_API_KEY = os.getenv("LAVA_API_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
