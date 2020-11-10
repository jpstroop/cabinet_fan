from adafruit_bme280 import Adafruit_BME280_I2C
from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from busio import I2C
from datetime import datetime
from digitalio import DigitalInOut
from time import sleep
import board

# TODO: read stuff from config file

SAMPLE_INTERVAL = 5 # minutes

i2c = I2C(board.SCL, board.SDA)
bme280 = Adafruit_BME280_I2C(i2c, address=0x76)

def sample_temp():
    return bme280.temperature * 1.8 + 32


# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Modify if connecting to different pins from 
# https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/wiring#wiring-diagram-1234506-8
lcd_rs = DigitalInOut(board.D22)
lcd_en = DigitalInOut(board.D17)
lcd_d4 = DigitalInOut(board.D25)
lcd_d5 = DigitalInOut(board.D24)
lcd_d6 = DigitalInOut(board.D23)
lcd_d7 = DigitalInOut(board.D18)

lcd = Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

lcd.clear()

temp = sample_temp()
now = datetime.now()
sample_minute = now.minute

while True:

    line_1 = now.strftime('%b %d %I:%M %p')
    line_2 = f'{round(temp, 1)} F'

    lcd.message = f'{line_1}\n{line_2}'

    if now.minute % SAMPLE_INTERVAL == 0 and now.minute != sample_minute:
        # TODO: log
        temp = sample_temp()
        sample_minute = now.minute

#    if temp >= MAX:
#        fan_on()
#    elif temp < MAX:
#        fan_off()

    now = datetime.now()
    sleep(1)
