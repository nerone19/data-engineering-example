import os
from models import Ship, get_engine
from utils import extractor_weather_date
from config import formatted_row_message, weather_collection
from sqlmodel import select, Session, func
from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta

app = Flask(__name__)
engine = get_engine()


@app.route("/ships", methods=["GET"])
def list_ships() -> Response:
    """
    Lists all the ships available in the db.
    """
    try:
        with Session(engine) as session:
            statement = select(Ship.device_id).distinct()
            result = session.execute(statement).scalars().all()
            return jsonify({"available data for the following ships ": result})
    except Exception as e:
        return jsonify({'Error':e}),500

@app.route("/ships/avg_speed/2019-02-13", methods=["GET"])
def list_avg_speed() -> Response:
    """
    Lists the avg speed for each boat in the date 2019-02-13.
    """
    with Session(engine) as session:
        
        start_date = datetime(2019, 2, 13)
        end_date = start_date + timedelta(days=1)
        
        statement = select(Ship.device_id, func.avg(formatted_row_message['speed'])).where(
            Ship.date_time >= start_date,
            Ship.date_time < end_date, 
        ).group_by(Ship.device_id)
        
        
        result = session.execute(statement).all()
        data = {}
        for r in result:
            device_id, avg_speed = r
            data[device_id] = avg_speed
            
    return data
    
@app.route("/ship/st-1a2090/daily_max_min_speed", methods=["GET"])
def daily_max_min_speed() -> Response:
    """
    Lists the min/max speed of one single boat on every day it traveled.
    """
    with Session(engine) as session:
        
        date_only = func.date(Ship.date_time)

        statement = select(date_only, func.max(formatted_row_message['speed']), func.min(formatted_row_message['speed'])).where(
            Ship.device_id == 'st-1a2090'
        ).group_by(date_only)
        
        result = session.execute(statement).all()
        data = {}
        for r in result:
            date, max_speed, min_speed = r
            day_of_the_year = date.strftime("%Y-%m-%d")
            data[day_of_the_year] = {'max_speed': max_speed, 'min_speed': min_speed}
    return data

@app.route("/ship/st-1a2090/route_weather/2019-02-13", methods=["GET"])
def fetch_daily_weather_conditions() -> Response:
    """
    Fetch the daily weather condition for one single boat on one single day..
    """
    with Session(engine) as session:
        
        start_date = datetime(2019, 2, 13)
        end_date = start_date + timedelta(days=1)
     
        statement = select(formatted_row_message["lat"],formatted_row_message["lon"], Ship.date_time).where(
            Ship.date_time >= start_date,
            Ship.date_time < end_date,
            Ship.device_id == 'st-1a2090', 
        ).order_by(Ship.date_time)
                
        result = session.execute(statement).all()
        trip_overview = []
        for r in result:
            lat, lon, date = r
            data_point = extractor_weather_date(float(lat), float(lon), date)
            if data_point:
                trip_overview.append(data_point)
                
    return trip_overview

@app.route("/health", methods=["GET"])
def health() -> Response:
    return "Healthy", 200

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
