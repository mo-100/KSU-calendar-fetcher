import datetime as dt

from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USER")
END_DATE = dt.datetime(2024, 5, 16 + 1)
