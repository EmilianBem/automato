from flask import Flask, render_template, request
from bme680 import bme680_out
from STEMMA_soil_sensor import stemma_out
import RPi.GPIO as GPIO

app = Flask(__name__)

RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

@app.route('/bme680')
def api_bme680_out():
	return bme680_out()

@app.route('/STEMMA_soil_sensor')
def api_stemma_out():
	return stemma_out()


@app.route('/')
def index():
	response = str(render_template('index.html'))
	return response

@app.route('/control', methods=['POST'])
def control():
    action = request.form['action']
    if action == 'on':
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    elif action == 'off':
        GPIO.output(RELAY_PIN, GPIO.LOW)
    return 'OK'

@app.route('/update_sensor_data')
def update_sensor_data():
    stemma_values = api_stemma_out()
    bme_values = api_bme680_out()
    response = (
        "Stemma: <br>Temp: " + str(stemma_values["Temperature"])
        + "<br>Moisture: " + str(stemma_values["Moisture"])
        + "<br><br> BME680: <br> Temp: " + str(bme_values["Temperature"])
        + "<br>Humidity: " + str(bme_values["Humidity"])
        + "<br> Pressure: " + str(bme_values["Pressure"])
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8123, debug=True)


if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0', port=8123, debug=True)
