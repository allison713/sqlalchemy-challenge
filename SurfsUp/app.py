## Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Mmt = Base.classes.measurement
Sta = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start  Type start date using YYYY-MM-DD format"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query data from last twelve months
    results = session.query(Mmt.date, Mmt.prcp).filter(Mmt.date >= '2016-08-23').all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all precipitation values
    precipitation_json = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precipitation_json.append(precip_dict)

    return jsonify(precipitation_json)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query data from last twelve months
    results = session.query(Sta.station, Sta.name, Sta.latitude, Sta.longitude, Sta.elevation).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all precipitation values
    station_json = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_json.append(station_dict)

    return jsonify(station_json)


@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query data from last twelve months
    last_row = session.query(Mmt.date).order_by(Mmt.date.desc()).first()
    last_date = dt.date.fromisoformat(last_row[0])
    query_date = last_date - dt.timedelta(days=365)
    results = session.query(Mmt.date, Mmt.tobs, Mmt.station).filter(Mmt.station == "USC00519281").filter(Mmt.date >= query_date).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all precipitation values
    tobs_json = []
    for date, tobs, station in results:
        tobs_dict = {}
        tobs_dict["station"] = station        
        tobs_dict[date] = tobs
        tobs_json.append(tobs_dict)

    return jsonify(tobs_json)


@app.route("/api/v1.0/<start>")
def temps_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Edit possible formatting variations
    corrected_start = start.replace("/","-").replace(" ","")
    
    # Query all temps
    temps = session.query(Mmt.date, Mmt.tobs).filter(Mmt.date >= corrected_start).all()

    tmin = session.query(Mmt.date, func.min(Mmt.tobs)).filter(Mmt.date >= corrected_start).all()
    tmax = session.query(Mmt.date, func.max(Mmt.tobs)).filter(Mmt.date >= corrected_start).all()
    tavg = session.query(Mmt.date, func.avg(Mmt.tobs)).filter(Mmt.date >= corrected_start).all()
    
    return jsonify(tmin, tmax, tavg)
    
    # tavg = session.query(Mmt.date, func.avg(Mmt.tobs)).filter(Mmt.date >= corrected_start).first()
    # tmax = session.query(Mmt.date, Mmt.tobs).filter(Mmt.date >= corrected_start).order_by(Mmt.tobs.desc()).first()
    # tobs_dict = {"TMIN":tmin, "TAVG":tavg, "TMAX":tmax}
    # tobs_json.append(tobs_dict)

    # return jsonify(tobs_json)

    session.close()


if __name__ == '__main__':
    app.run(debug=True)