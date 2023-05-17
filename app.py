from flask import Flask, render_template
from bme680 import bme680_out
from STEMMA_soil_sensor import stemma_out

app = Flask(__name__)

@app.route('/bme680')
def api_bme680_out():
	return bme680_out()

@app.route('/STEMMA_soil_sensor')
def api_stemma_out():
	return stemma_out()

@app.route('/')
def index():
	stemma_values = api_stemma_out()
	bme_values = api_bme680_out()
	response = str(render_template('index.html')) + "Stemma: <br>Temp: "+ str(stemma_values["Temperature"]) + "<br>Moisture: " + str(stemma_values["Moisture"])
	#response = str(render_template('index.html')) + "Stemma: <br>Temp: " + str(bme_values)
	#response = "dupa"
	return response


if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0', port=8123, debug=True)
