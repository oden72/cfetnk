# ssd1306_setup.py Demo pogram for rendering arbitrary fonts to an SSD1306 OLED display.
# ssd1306_setup.py Device initialisation. Copy to color_setup.py on host.

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2018-2021 Peter Hinch


# https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x32-spi-oled-display
# https://www.proto-pic.co.uk/monochrome-128x32-oled-graphic-display.html

import machine
from drivers.ssd1306.ssd1306 import SSD1306_I2C as SSD

WIDTH = const(128)
HEIGHT = const(64)
soft = False  # Soft or hard I2C/SPI

# Export an initialised ssd display object.
# pico   SSD
# 3v3   Vin
# Gnd   Gnd
# 21    CLK
# 20   DATA
if soft:
    pscl = machine.Pin(21, machine.Pin.OPEN_DRAIN)
    psda = machine.Pin(20, machine.Pin.OPEN_DRAIN)
    i2c = machine.SoftI2C(scl=pscl, sda=psda)
else:
    pscl = machine.Pin(3)
    psda = machine.Pin(2)
    i2c = machine.I2C(1, scl=pscl, sda=psda)
ssd = SSD(WIDTH, HEIGHT, i2c)
