import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///SurfsUp/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with = engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def home():
    return(
        "Available routes :<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).where(Measurement.date>="2016-08-23")
    session.close()
    precipitation_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precipitation_list.append(prcp_dict)
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_names = session.query(Measurement.station).distinct().all()
    session.close()
    station_list = list(np.ravel(station_names))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active = engine.execute('SELECT station, COUNT(station) AS "Frequency count" \
                            FROM Measurement \
                            GROUP BY station \
                            ORDER BY "Frequency count" DESC;').first()
    temps = session.query(Measurement.tobs).filter(Measurement.station == most_active[0]).all()
    session.close()
    tobs_list = list(np.ravel(temps))
    return jsonify(tobs_list)

if __name__ == "__main__":
    app.run(debug=True)