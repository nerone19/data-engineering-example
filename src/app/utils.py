from typing import Dict

from config import  weather_collection

def extractor_weather_date(latitude: float, longitude: float,date: str) -> Dict:
    """
    Extract weather data records matching with the input method parameters (same coordinates and date).
    We consider the match up to the same hour (not minute or seconds).

    Args:
        latitude (float): the latitude for the searched match.
        longitude (float): the longitude for the searched match.
        date (str):  the datetime for the searched match.

    Returns:
        Dict: A dictionary containing the matched weather conditions from the no-sql database.
    """
    try:
        datetime_utc = date.strftime("%Y-%m-%dT%H")
        data_point = weather_collection.find_one({"lat": float(latitude), "lon": float(longitude)})
        daily_weather = {}
        if data_point:
            for el in data_point['data']:
                if datetime_utc in el["timestamp_utc"]:
                    daily_weather = {
                        "time" : el['timestamp_utc'],
                        "wind_speed" : el['wind_spd'],
                        "weather description" : el['weather']['description'],
                        "temperature" : el['temp']
                    }
                    break
                        
    except Exception as e:
        print(e)
    finally:
        return daily_weather