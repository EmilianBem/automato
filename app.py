from flask import Flask, render_template, request
from bme680 import bme680_out
from STEMMA_soil_sensor import stemma_out
from db_insert_data import insert_data
from db_get_data import get_db_data
import RPi.GPIO as GPIO
import time
import asyncio
import threading

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
    data_insert_thread = threading.Thread(target=insert_data)
    data_insert_thread.start()

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


@app.route('/get_db_temp_data')
def get_db_temp_data():
    data_query_thread = threading.Thread(target=get_db_data)
    data_query_thread.start()
    data_query_thread.join()
    response = (
        data_query_thread
    )
    return response


def trigger_fan_from_humidity_on_sensor():
    try:
        while True:
            bme_values = api_bme680_out()
            if bme_values["Humidity"] > 40:
                print(bme_values["Humidity"])
                GPIO.output(RELAY_PIN_FAN, GPIO.HIGH)
            elif bme_values["Humidity"] < 40:
                GPIO.output(RELAY_PIN_FAN, GPIO.LOW)
                time.sleep(5)  # check sensor every 5s
            time.sleep(10)  # Delay to avoid rapid reading
    except KeyboardInterrupt:
        pass


def trigger_lights_periodically():
    try:
        while True:
            GPIO.output(RELAY_PIN_LIGHTS_1, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(RELAY_PIN_LIGHTS_1, GPIO.LOW)
            time.sleep(1)

    except KeyboardInterrupt:
        pass


def trigger_water_pump_from_moisture_on_sensor():
    try:
        while True:
            stemma_values = api_stemma_out()
            if stemma_values["Moisture"] > 600:
                GPIO.output(RELAY_PIN_WATER_PUMP, GPIO.HIGH)
            elif stemma_values["Moisture"] < 400:
                GPIO.output(RELAY_PIN_WATER_PUMP, GPIO.LOW)
                time.sleep(1)  # check sensor every 1s while watering
            time.sleep(5)  # Delay to avoid rapid reading
    except KeyboardInterrupt:
        pass


def trigger_water_pump_from_moisture_on_sensor():
    try:
        while True:
            stemma_values = api_stemma_out()
            if stemma_values["Moisture"] > 600:
                GPIO.output(RELAY_PIN_WATER_PUMP, GPIO.HIGH)
            elif stemma_values["Moisture"] < 400:
                GPIO.output(RELAY_PIN_WATER_PUMP, GPIO.LOW)
                time.sleep(1)  # check sensor every 1s while watering
            time.sleep(5)  # Delay to avoid rapid reading
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':

    water_pump_thread = threading.Thread(target=trigger_water_pump_from_moisture_on_sensor)
    fan_thread = threading.Thread(target=trigger_fan_from_humidity_on_sensor)
    lights_thread = threading.Thread(target=trigger_lights_periodically)

    water_pump_thread.start()
    fan_thread.start()
    lights_thread.start()

    app.run(host='0.0.0.0', port=8123, debug=True)

    try:
        # Keep the main program running
        while True:
            pass
    except KeyboardInterrupt:
        # Clean up GPIO settings
        GPIO.cleanup()
