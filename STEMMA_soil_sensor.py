# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ss = Seesaw(i2c_bus, addr=0x36)


def stemma_out():
    moisture = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()

    stemma_reading = {
        "Temperature": temp,
        "Moisture": moisture
    }
    return stemma_reading    # read moisture level through capacitive touch pad
