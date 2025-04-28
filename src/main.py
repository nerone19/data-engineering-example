import csv
import json
import os

from sqlmodel import Session
from datetime import datetime 
from pymongo import MongoClient

from models import Ship, get_engine

engine = get_engine()


def get_mongo_client() -> MongoClient:
    """return the mongo client for connecting to Mongo.

    Returns:
        The MongoClient.
    """
    return MongoClient(os.getenv("MONGO_URI"))

def extract_raw_messages() -> None:
    """
    Extract the messages sent by the device on the Ship data.
    
    returns: 
        None
    """
    with open('./preprocessed_messages.csv', newline='') as csvfile:

        reader = csv.reader(csvfile, delimiter=',', doublequote=True, quotechar='"')

        for i,row in enumerate(reader, 1):
            device_id, date_time, address_ip, address_port, original_message_id, raw_message = row

            with Session(engine) as session:
                try:
                    ship = Ship(device_id=device_id, 
                                date_time=datetime.fromtimestamp(int(date_time)), 
                                address_ip=address_ip, 
                                address_port=int(address_port), 
                                original_message_id=original_message_id, 
                                raw_message=raw_message)
                    session.add(ship)
                    session.commit()
                except Exception as e:
                    print(f"Error: {e}")
                    session.rollback()
                    continue


def extractor_weather_date() -> None:
    """
    Extract data about the weather.
    """
    try:
        client = get_mongo_client()
        db = client.test
        weather_collection = db.get_collection("weather_collection")
        
        with open('./weather_data.json', 'r') as file:
            data = json.load(file)
            for line in data:
                weather_collection.insert_one(line)

    except Exception as e:
        print(f"Error: {e}")         


def main():
    print('starting the data extraction.', flush=True)
    extract_raw_messages()
    extractor_weather_date()       
    print('Data extraction completed. The dbs have been now populated.', flush=True) 

main()
