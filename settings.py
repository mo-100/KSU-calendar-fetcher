import datetime as dt

from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USER")
END_DATE = dt.datetime(2023, 12, 7 + 1)
