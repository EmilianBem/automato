from flask import Flask, render_template, request
from bme680 import bme680_out
from STEMMA_soil_sensor import stemma_out
import RPi.GPIO as GPIO

app = Flask(__name__)

RELAY_PIN_FAN = 22
RELAY_PIN_LIGHTS_1 = 23
RELAY_PIN_LIGHTS_2 = 27
RELAY_PIN_WATER_PUMP = 17

device_pin_map = {
    'fan': RELAY_PIN_FAN,
    'light-1': RELAY_PIN_LIGHTS_1,
    'light-2': RELAY_PIN_LIGHTS_2,
    'water-pump': RELAY_PIN_WATER_PUMP
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN_FAN, GPIO.OUT)
GPIO.setup(RELAY_PIN_LIGHTS_1, GPIO.OUT)
GPIO.setup(RELAY_PIN_LIGHTS_2, GPIO.OUT)
GPIO.setup(RELAY_PIN_WATER_PUMP, GPIO.OUT)

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

@app.route('/control-devices', methods=['POST'])
def control_devices():
    req = request.form['action']
    action = req[-1]
    device = req[:-2]
    if device in device_pin_map:
        pin = device_pin_map[device]
    else:
        return 'Invalid device'

    if action == '0':
        GPIO.output(pin, GPIO.HIGH)
    elif action == '1':
        GPIO.output(pin, GPIO.LOW)
    else:
        return 'Invalid action'

    return str(render_template('index.html'))

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
