from flask import Flask, render_template, request
from bme680 import bme680_out
from STEMMA_soil_sensor import stemma_out
import RPi.GPIO as GPIO

app = Flask(__name__)

# Konfiguracja pinów dla urządzeń
DEVICE_PINS = {
    "device1": 23,
    "device2": 22,
    "device3": 27,
    "device4": 17
}

# Inicjalizacja pinów GPIO
GPIO.setmode(GPIO.BCM)
for pin in DEVICE_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

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
    device = request.form['device']
    
    if action == 'on':
        GPIO.output(DEVICE_PINS[device], GPIO.HIGH)
    elif action == 'off':
        GPIO.output(DEVICE_PINS[device], GPIO.LOW)
    
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
