## Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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
        f"/api/v1.0/stations"
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


########
##NOT WORKING
#######
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query data from last twelve months
    results = session.query(Sta.station).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all precipitation values
    station_json = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict['name'] = name
        # station_dict["latitude"] = latitude
        # station_dict["longitude"] = longitude
        # station_dict["elevation"] = elevation
        station_json.append(station_dict)

    return jsonify(station_json)


if __name__ == '__main__':
    app.run(debug=True)