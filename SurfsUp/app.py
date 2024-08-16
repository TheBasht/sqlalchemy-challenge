# Import the dependencies.
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import datetime as dt
import numpy as np


#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

#reflect the tables
Base.prepare(autoload_with=engine)

print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Flask Setup
#################################################

# Create an instance of Flask
app = Flask(__name__)

# Define the routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfs Up API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    station_list = []
    for station, name in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count().desc()).\
        first()
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station[0]).\
        filter(Measurement.date >= last_year).all()

    # Convert the query results to a list of dictionaries
    temperature_list = []
    for date, tobs in temperature_data:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["tobs"] = tobs
        temperature_list.append(temperature_dict)

    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query the minimum, average, and maximum temperatures for a given start date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert the query results to a list of dictionaries
    temperature_stats_list = []
    for min_temp, avg_temp, max_temp in temperature_stats:
        temperature_stats_dict = {}
        temperature_stats_dict["min_temp"] = min_temp
        temperature_stats_dict["avg_temp"] = avg_temp
        temperature_stats_dict["max_temp"] = max_temp
        temperature_stats_list.append(temperature_stats_dict)

    return jsonify(temperature_stats_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query the minimum, average, and maximum temperatures for a given start-end range
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Convert the query results to a list of dictionaries
    temperature_stats_list = []
    for min_temp, avg_temp, max_temp in temperature_stats:
        temperature_stats_dict = {}
        temperature_stats_dict["min_temp"] = min_temp
        temperature_stats_dict["avg_temp"] = avg_temp
        temperature_stats_dict["max_temp"] = max_temp
        temperature_stats_list.append(temperature_stats_dict)

    return jsonify(temperature_stats_list)


if __name__ == '__main__':
    app.run(debug=True)