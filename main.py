from adafruit_bmp280 import Adafruit_BMP280_SPI
from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from atexit import register as exit_callback
from busio import SPI
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

def configure_bmp280s(config):
    spi0 = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs0 = DigitalInOut(getattr(board, f"D{config['bmp280'].get('cs0', 5)}"))
    sensor0 = Adafruit_BMP280_SPI(spi0, cs0)

    spi1 = SPI(board.SCK_1, MOSI=board.MOSI_1, MISO=board.MISO_1)
    cs1 = DigitalInOut(getattr(board, f"D{config['bmp280'].get('cs1', 6)}"))
    sensor1 = Adafruit_BMP280_SPI(spi1, cs1)

    return (sensor0, sensor1)

def sample_temp(bmp280):
    temp_f = bmp280.temperature * 1.8 + 32
    return temp_f

def shutdown(fan, lcd, log=False):
    # TODO: can we also cut power to the LCD?
    if log:
        print(f'{dt.now()} shutting down...', end='' )
    lcd.clear()
    fan.off()
    if log:
        print(f'Done')

def run(config, bmp280_0, bmp280_1, lcd, fan, log=False):
    '''bmp280_0 should will turn the fan on and off, bmp280_1 is on the board and will
    report the ambient temperature.
    '''
    sample_interval = config.get('sample_interval', 5)
    temp = sample_temp(bmp280_0)
    now = dt.now()
    sample_minute = now.minute
    while True:
        line_1 = f'Room: {round(sample_temp(bmp280_1), 1)} F'
        line_2 = f'Cabinet: {round(temp, 1)} F'
        lcd.message = f'{line_1}\n{line_2}'
        if now.minute % sample_interval == 0 and now.minute != sample_minute:
            temp = sample_temp(bmp280_0)
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
        self.power.direction = Direction.OUTPUT
        self.power.value = False

    def on(self):
        self.power.value = True

    def off(self):
        self.power.value = False


if __name__ == "__main__":
    config = load_config(find_config())
    bmp280_0, bmp280_1 = configure_bmp280s(config)
    lcd = configure_lcd(config)
    fan = Fan(config)
    exit_callback(shutdown, fan, lcd, log=True)
    run(config, bmp280_0, bmp280_1, lcd, fan, log=True)

