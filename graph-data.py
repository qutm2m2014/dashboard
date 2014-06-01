from flask import Response, json, Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://m2m:@m2m2014@pg.qutm2m.com:5432/m2m'
app.config["SQLALCHEMY_ECHO"] = True
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
	data = tempData.query.all()
	temp_list = [['Time', 'Temprature']]
	for atom in data:
		atoms = [atom.rDate, atom.temp]
		temp_list.append(atoms)
	return render_template("graph.html", temp_list = temp_list)
      

if __name__ == "__main__":

    app.run(host= 'localhost', port=3000)