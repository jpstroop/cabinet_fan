from adafruit_bmp280 import Adafruit_BMP280_SPI
from adafruit_character_lcd.character_lcd import Character_LCD_RGB
from atexit import register as register_exit_callback
from busio import SPI
from datetime import datetime as dt
from digitalio import DigitalInOut
from digitalio import Direction
from json import load
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import expanduser
from os.path import join
from pulseio import PWMOut
from time import sleep
import board

from lcd import configure_lcd

class App()
    def __init__(self):
        config = App._load_config()
        sensor_config = config['temp_sensors']
        self.onboard_sensor = TempSensor(sensor_config['onboard_pin'], 0)
        self.cabinet_sensor = TempSensor(sensor_config['cabinet_pin'], 1)
        self.lcd = configure_lcd(config['lcd'])
        self.fan = Fan(config['fan']['power_pin'])
        self.sample_interval = config['app']['sample_interval']
        self.max_temp = config['app']['max_temp']
        register_exit_callback(self._shutdown())

    def _shutdown(self):
        self.lcd.clear()
        # TODO: turn off LCD??
        self.fan.off()

    @staticmethod
    def _load_config():
        pth = App._find_config()
        with open(pth) as f:
            config = load(f)
            return config

    @staticmethod
    def _find_config(self):
        '''~/cabinet_fan.json will override ./config.json, but the assumption
        is that ~/cabinet_fan.json will contain all values; there is no inheritance.
        '''
        local = join(expanduser('~'), 'cabinet_fan.json')
        sibling = join(dirname(__file__), 'config.json')
        if exists(local):
            return local
        else:
            return sibling

    def run(self):
        cabinet_temp = self.cabinet_sensor.sample_temp()
        now = dt.now()
        sample_minute = now.minute
        while True:
            line_1 = now.strftime('%b %d %I:%M %p')
            # TODO: create a degree character
            line_2 = f'Internal: {cabinet_temp)} F'
            line_3 = f'Outside: {self.onboard_sensor.sample_temp()} F'
            lcd.message = f'{line_1}\n{line_2}\n{line_3}'
            if now.minute % self.sample_interval == 0 and now.minute != sample_minute:
                cabinet_temp = self.cabinet_sensor.sample_temp()
                sample_minute = now.minute
                # TODO: set background color based on cabinet_temp
                if cabinet_temp > self.max_temp:
                     fan.on()
                elif cabinet_temp <= self.max_temp:
                     fan.off()
            now = dt.now()
            sleep(1)

class TempSensor():
    def __init__(self, pin_no, spi_interface):
        spi = None
        if spi_interface == 0:
            spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        elif spi_interface == 1:
            spi = SPI(board.SCK_1, MOSI=board.MOSI_1, MISO=board.MISO_1)
        pin = getattr(board, f'D{pin_no}')
        cs = DigitalInOut(pin)
        self.sensor = Adafruit_BMP280_SPI(spi, cs)

    def sample_temp(unit='F'):
        if unit == 'F':
            return round(bmp280.temperature * 1.8 + 32, 1)
        else:
            return round(bmp280.temperature, 1)

class Fan():
    def __init__(self, power_pin):
        self.power = DigitalInOut(getattr(board, f'D{power_pin}'))
        self.power.direction = Direction.OUTPUT
        self.power.value = False

    def on(self):
        self.power.value = True

    def off(self):
        self.power.value = False


if __name__ == "__main__":
    app = App()
    app.run()
