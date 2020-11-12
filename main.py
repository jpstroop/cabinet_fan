from adafruit_bme280 import Adafruit_BME280_I2C
from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from atexit import register as exit_callback
from busio import I2C
from datetime import datetime as dt
from digitalio import DigitalInOut
from digitalio import Direction
from importlib import import_module
from json import load
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import expanduser
from os.path import join
from time import sleep
import board
import RPi.GPIO as gpio

def find_config():
    '''~/cabinet_fan.json will override ./config.json, but the assumption
    is that ~/cabinet_fan.json will contain all values; there is no inheritance.
    '''
    local = join(expanduser('~'), 'cabinet_fan.json')
    sibling = join(dirname(__file__), 'config.json')
    if exists(local):
        return local
    else:
        return sibling

def load_config(pth):
    with open(pth) as f:
        config = load(f)
    return config

def configure_lcd(config, cols=16, rows=2):
    rs = DigitalInOut(getattr(board, f"D{config['lcd'].get('rs', 22)}"))
    en = DigitalInOut(getattr(board, f"D{config['lcd'].get('en', 17)}"))
    d4 = DigitalInOut(getattr(board, f"D{config['lcd'].get('d4', 25)}"))
    d5 = DigitalInOut(getattr(board, f"D{config['lcd'].get('d5', 24)}"))
    d6 = DigitalInOut(getattr(board, f"D{config['lcd'].get('d6', 23)}"))
    d7 = DigitalInOut(getattr(board, f"D{config['lcd'].get('d7', 18)}"))
    lcd = Character_LCD_Mono(rs, en, d4, d5, d6, d7, cols, rows)
    lcd.clear()
    return lcd

def configure_bme289(config):
    # TODO Allow choice of I2C or SPI?
    address = int(config.get('bme280_address', "0x77"), 16) # hex value is stored as a str
    i2c = I2C(board.SCL, board.SDA)
    return Adafruit_BME280_I2C(i2c, address=address)

def sample_temp(bme280, log=False):
    temp_f = bme280.temperature * 1.8 + 32
    if log:
        print(f'{dt.now() } sample: {temp_f}')
    return temp_f

def shutdown(fan, lcd, log=False):
    # TODO: can we also cut power to the LED?
    if log:
        print(f'{dt.now()} shutting down...', end='' )
    lcd.clear()
    fan.off()
    if log:
        print(f'Done')

def run(config, bme280, lcd, fan, log=False):
    sample_interval = config.get('sample_interval', 5)
    temp = sample_temp(bme280, log)
    now = dt.now()
    sample_minute = now.minute
    while True:
        line_1 = now.strftime('%b %d %I:%M %p') # TODO: make configurable
        line_2 = f'{round(temp, 1)} F'
        lcd.message = f'{line_1}\n{line_2}'
        if now.minute % sample_interval == 0 and now.minute != sample_minute:
            temp = sample_temp(bme280, log)
            sample_minute = now.minute
            if temp > fan.max_temp:
                 fan.on()
            elif temp <= fan.max_temp:
                 fan.off()
        now = dt.now()
        sleep(1)

class Fan():
    def __init__(self, config):
        self.max_temp = config["fan"].get("max_temp", 78)
        self.power = DigitalInOut(getattr(board, f"D{config['fan'].get('power_pin', 15)}"))
        power.direction = Direction.OUTPUT
        power.value = False

    def on(self):
        power.value = True

    def off(self):
        power.value = False


if __name__ == "__main__":
    config = load_config(find_config())
    bme280 = configure_bme289(config)
    lcd = configure_lcd(config)
    fan = Fan(config)
    exit_callback(shutdown, fan, lcd, log=True)
    run(config, bme280, lcd, fan, log=True)

