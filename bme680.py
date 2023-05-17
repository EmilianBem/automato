
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bme680

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c,0x77)

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

#while True:
#	 print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
#	 print("Humidity: %0.1f %%" % bme680.relative_humidity)
#	 print("Pressure: %0.3f hPa" % bme680.pressure)
#	 time.sleep(1)


def bme680_out():
	bme680_reading = {
		"Temperature": bme680.temperature,
		"Humidity": bme680.relative_humidity,
		"Pressure": bme680.pressure
	}
	return bme680_reading
