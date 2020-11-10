from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from bme280 import load_calibration_params
from bme280 import sample
from datetime import datetime
from digitalio import DigitalInOut
from smbus2 import SMBus
from time import sleep
import board

# TODO: read stuff from config file

SAMPLE_INTERVAL = 5 # minutes

address = int("0x76", 16) # Change to 0x77 if necessary
bus = SMBus(1) # Change arg if bme 280 is connected to a different port (than 1)
calibration_params = load_calibration_params(bus, address)

def sample_temp():
    data = sample(bus, address, calibration_params)
    return data.temperature * 1.8 + 32


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
        print("sampling...")
        print(now)
        temp = sample_temp()
        sample_minute = now.minute

#    if temp >= MAX:
#        fan_on()
#    elif temp < MAX:
#        fan_off()

    now = datetime.now()
    sleep(1)
