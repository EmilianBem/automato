from flask import Flask, render_template, request
from bme680 import bme680_out
from STEMMA_soil_sensor import stemma_out
import RPi.GPIO as GPIO
import time

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

def get_measurements():
    stemma_values = api_stemma_out()
    bme_values = api_bme680_out()
    return {
        "stemma_temperature": stemma_values["Temperature"],
        "stemma_moisture": stemma_values["Moisture"],
        "bme_temperature": bme_values["Temperature"],
        "bme_humidity": bme_values["Humidity"],
        "bme_pressure": bme_values["Pressure"]
    }

@app.route('/')
def index():
    measurements = get_measurements()
    response = str(render_template('index.html')) + "Stemma: <br>Temp: " + str(measurements["stemma_temperature"]) + "<br>Moisture: " + str(measurements["stemma_moisture"]) + "<br><br> BME680: <br> Temp: " + str(measurements["bme_temperature"]) + "<br>Humidity: " + str(measurements["bme_humidity"]) + "<br> Pressure: " + str(measurements["bme_pressure"])
    return response

@app.route('/control', methods=['POST'])
def control():
    action = request.form['action']
    if action == 'on':
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    elif action == 'off':
        GPIO.output(RELAY_PIN, GPIO.LOW)
    return 'OK'

if __name__ == '__main__':
    # Oczekiwanie na dostępność pomiarów
    while True:
        measurements = get_measurements()
        if all(measurements.values()):
            break
        time.sleep(0.1)  # Dostosuj czas oczekiwania, jeśli trzeba
    app.run(host='0.0.0.0', port=8123, debug=True)
