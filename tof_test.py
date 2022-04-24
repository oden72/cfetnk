from machine import Pin, I2C
from vl53l0x import VL53L0X
import time
import af_ssd1306
from color_setup import ssd
from gui.core.nanogui import refresh
from gui.widgets.label import Label
from gui.core.writer import Writer
import gui.fonts.arial35 as arial35

CAL_INTERCEPT = 80
CAL_SLOPE = 1


def map(x):
    # full tank is 10, empty is 220
    r = max(10, x)
    r = min(r, 220)
    r = (r - 10) / 210
    return 100 * (1 - r)


def test():
    print("setting up i2c")
    sda = Pin(0)
    scl = Pin(1)
    id = 0

    i2c = I2C(id=id, sda=sda, scl=scl)

    print(i2c.scan())

    # print("creating vl53lox object")
    # Create a VL53L0X object
    tof = VL53L0X(i2c, address=41)

    # Pre: 12 to 18 (initialized to 14 by default)
    # Final: 8 to 14 (initialized to 10 by default)

    # the measuting_timing_budget is a value in ms, the longer the budget, the more accurate the reading.
    budget = tof.measurement_timing_budget_us
    print("Budget was:", budget)
    tof.set_measurement_timing_budget(800000)

    # Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the
    # given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange)
    # to the given value (in PCLKs). Longer periods increase the potential range of the sensor.
    # Valid values are (even numbers only):

    # tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

    # tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)
    i = tof.ping()
    while i > 1000:
        i = tof.ping()
    val = i

    stop_pin = Pin(13, mode=Pin.IN, pull=Pin.PULL_UP)
    ssd.fill(0)
    refresh(ssd)
    Writer.set_textpos(ssd, 0, 0)
    wri = Writer(ssd, arial35, verbose=False)
    wri.set_clip(True, True, False)
    text = "  0%"
    tf = Label(wri, 0, 2, wri.stringlen(text))
    tf.value(text)
    refresh(ssd)

    while stop_pin.value():
        # Start ranging
        new = (tof.ping() - CAL_INTERCEPT) / CAL_SLOPE
        if new > 1000:
            new = val
        val = 0.8 * val + 0.2 * new
        vol = map(val)
        text = f"{vol:3.0f}%"
        print(new, val, " mm", text)
        ssd.fill(0)
        tf.value(text)
        refresh(ssd)
        time.sleep(10)

    text = "EXT"
    ssd.fill(0)
    tf.value(text)
    refresh(ssd)


def testscr():
    print("setting up i2c for screen")
    sda = Pin(2)
    scl = Pin(3)
    id = 1

    i2c = I2C(id=id, sda=sda, scl=scl)

    print(i2c.scan())
    oled_w = 128
    oled_h = 64
    oled = af_ssd1306.SSD1306_I2C(oled_w, oled_h, i2c)

    oled.text('Hello World 1', 0, 0)
    oled.text('Hello World 2', 0, 10)
    oled.text('Hello World 3', 0, 20)

    oled.show()


def teststop():
    stop_pin = Pin(13, mode=Pin.IN, pull=Pin.PULL_UP)
    while stop_pin.value():
        print('working...')
        time.sleep(2)

    print('stopping...')
