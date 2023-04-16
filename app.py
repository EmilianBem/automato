from flask import Flask
from bme280_out import bme280
from stemma_out import STEMMA_soil_sensor

app = Flask(__name__)

@app.route('/bme280')
def bme280_out():
    return bme280_out()

@app.route('/STEMMA_soil_sensor')
def stemma_out():
    return stemma_out()

if __name__ == '__main__':
    app.run(debug=True)