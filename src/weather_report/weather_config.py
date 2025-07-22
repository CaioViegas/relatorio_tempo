import os
from dotenv import load_dotenv

load_dotenv()

LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")
TIMEZONE = os.getenv("TIMEZONE")