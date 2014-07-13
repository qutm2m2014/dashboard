from flask import Flask, render_template, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from .config import DevConfig, ProductionConfig
import os
import redis


def configure_app(app):
    if os.environ.get("APP_ENV") is "PRODUCTION":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevConfig)


app = Flask(__name__)
configure_app(app)
db = SQLAlchemy(app)
red = redis.StrictRedis()


def event_stream(topic):
    pubsub = red.pubsub()
    pubsub.subscribe(topic)
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']


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
    temp_list = [['Time', 'Temprature']]
    for atom in data:
        atoms = [atom.rDate, atom.temp]
        temp_list.append(atoms)
    return render_template("index.html", temp_list=temp_list)


@app.route('/notifications')
def stream():
    return Response(event_stream('chat'), mimetype="text/event-stream")


@app.route("/notify", methods=["POST"])
def get_nofify():
    red.publish('chat', u'%s' % (request.form["message"]))
    print(request.form["topic"])
    if request.form["topic"] == "ERROR":
        red.publish('smartscreen', u'%s' % "/static/images/cooldown.jpg")
    else:
        red.publish('smartscreen', u'%s' % "/static/images/warmup.jpg")
    return Response(status=204)


@app.route("/smartscreen")
def show_screen():
    return render_template('smartscreen.html')


@app.route("/screenloader")
def loader():
    return Response(event_stream('smartscreen'), mimetype="text/event-stream")
