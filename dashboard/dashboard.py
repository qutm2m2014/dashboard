from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import DevConfig, ProductionConfig
import os


def configure_app(app):
    if os.environ.get("DASHBOARD_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevConfig)
    return app


app = Flask(__name__)
configure_app(app)
db = SQLAlchemy(app)


class tempData(db.Model):
    __tablename__ = 'raw_data'
    id = db.Column('dp_id', db.Integer, primary_key=True)
    atomId = db.Column('atom_id', db.Integer)
    sensorId = db.Column('sensor_id', db.Integer)
    rDate = db.Column('dt_created', db.DateTime(timezone=False))
    temp = db.Column('value', db.Float)


@app.route("/")
def send_data():
    data = reversed(tempData.query.order_by(tempData.rDate.desc()).limit(10).all())
    temp_list = []
    for atom in data:
        atoms = {"date": atom.rDate.strftime("%a, %d %b %Y %H:%M:%S"), "temp": atom.temp}
        temp_list.append(atoms)
    return render_template("index.html", temp_list=temp_list)
