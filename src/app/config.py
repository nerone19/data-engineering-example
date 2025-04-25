from typing import Dict, Tuple, Union
from pymongo import MongoClient

from sqlmodel import func, cast, Float, Text, DECIMAL, Numeric
from models import Ship

import os


raw_message_configuration = {
    "speed": (6,Float),
    "lat": (2, DECIMAL),
    "lon": (4, DECIMAL)
}

def fetch_from_raw_message(columns: Dict[str,Union[Tuple[int, Numeric], cast]]):
    raw_message_text = cast(Ship.raw_message, Text)
       
    for field, column in columns.items():
        
        columns[field] = cast(
            func.split_part(raw_message_text, ',', column[0]), column[1]
        )
    return columns

formatted_row_message = fetch_from_raw_message(raw_message_configuration)

mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client.test
weather_collection = mongo_db.get_collection("weather_collection")