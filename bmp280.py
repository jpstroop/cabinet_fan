from adafruit_bmp280 import Adafruit_BMP280_SPI
from busio import SPI
from digitalio import DigitalInOut
import board

class TempSensor():
    def __init__(self, cs_pin, miso_pin, mosi_pin,sclk_pin):
        spi = SPI(sclk_pin, MOSI=mosi_pin, MISO=miso_pin)
        cs = DigitalInOut(getattr(board, f'D{cs_pin}'))
        self.sensor = Adafruit_BMP280_SPI(spi, cs)

    def sample_temp(self, unit='F'):
        if unit == 'F':
            return round(self.sensor.temperature * 1.8 + 32, 1)
        else:
            return round(self.sensor.temperature, 1)

if __name__ == '__main__':
    from time import sleep

    sample_config = {
        "cs_pin" : 5,
        "mosi_pin" : 10,
        "miso_pin" : 9,
        "sclk_pin" : 11
    }
    sensor =  TempSensor(**sample_config)

    sample_config1 = {
        "cs_pin" : 6,
        "mosi_pin" : 10,
        "miso_pin" : 9,
        "sclk_pin" : 11
    }
    sensor1 =  TempSensor(**sample_config1)

    run_for = 10 #seconds
    print(f'Each sensor will sample the temperature about every second for about {run_for} seconds')
    sleep(2)
    count = 0
    while count < run_for:
        print(f'{count+1}: Sensor 0: {sensor.sample_temp()} F')
        print(f'{count+1}: Sensor 1: {sensor1.sample_temp()} F')
        sleep(1)
        count+=1
