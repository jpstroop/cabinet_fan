from adafruit_character_lcd.character_lcd import Character_LCD_RGB
from digitalio import DigitalInOut
from pulseio import PWMOut
import board

DEGREE_CHAR = '\x00'
UP_ARROW_CHAR = '\x01'
DOWN_ARROW_CHAR = '\x02'

#TODO: come up with a more pleasing spectrum.
COLD_TO_WARM = {
    73 : (0,0,255),
    74 : (0,148,255),
    75 : (0,196,255),
    76 : (0,228,255),
    77 : (0,255,168),
    78 : (0,255,16),
    79 : (176,255,0),
    80 : (255,250,0),
    81 : (255,220,0),
    82 : (255,180,0),
    83 : (255,150,0),
    84 : (255,120,0),
    85 : (255,0,0)
}

def config_lcd(config, cols=20, rows=4):
    rs = DigitalInOut(getattr(board, f"D{config.get('rs', 22)}"))
    en = DigitalInOut(getattr(board, f"D{config.get('en', 17)}"))
    d4 = DigitalInOut(getattr(board, f"D{config.get('d4', 25)}"))
    d5 = DigitalInOut(getattr(board, f"D{config.get('d5', 24)}"))
    d6 = DigitalInOut(getattr(board, f"D{config.get('d6', 23)}"))
    d7 = DigitalInOut(getattr(board, f"D{config.get('d7', 18)}"))
    red = PWMOut(getattr(board, f"D{config.get('r', 16)}"))
    green = PWMOut(getattr(board, f"D{config.get('g', 12)}"))
    blue = PWMOut(getattr(board, f"D{config.get('b', 13)}"))
    lcd = Character_LCD_RGB(rs, en, d4, d5, d6, d7, cols, rows, red, green, blue)

    # Degree Character
    lcd.create_char(0, (0x1c,0x14,0x1c,0x0,0x0,0x0,0x0,0x0))
    lcd.create_char(1, (0x4,0xe,0x15,0x4,0x4,0x4,0x4,0x4))
    lcd.create_char(2, (0x4,0x4,0x4,0x4,0x4,0x15,0xe,0x4))

    lcd.clear()
    return lcd

def expand_color(c):
    '''c is a colour.Color object'''
    return list(map(lambda p: int(p*100), (c.red, c.green, c.blue)))




if __name__ == '__main__':
    from time import sleep
    from colour import Color

    sample_config = {
        "rs" : 22,
        "en" : 17,
        "d4" : 7,
        "d5" : 24,
        "d6" : 23,
        "d7" : 8,
        "r" : 16,
        "g" : 12,
        "b" : 13
    }

    lcd = config_lcd(sample_config)
    degree_char = lcd.create_char(0x00, (0x1c,0x14,0x1c,0x0,0x0,0x0,0x0,0x0))
    lcd.message = "Hello\nWorld\nWe're going to\nrun some tests"
    sleep(1)
    lcd.clear()
    lcd.message = "In a moment, the\nbackground will\nturn red"
    sleep(1)
    lcd.color = (100, 0, 0)
    lcd.clear()
    lcd.message = "...next green"
    sleep(1)
    lcd.color = (0, 100, 0)
    lcd.message = "...and finally blue!"
    sleep(1)
    lcd.color = (0, 0, 100)
    sleep(1)
    lcd.clear()
    lcd.message = "Now the screen\nwill go from cold\nto warm and back"
    sleep(1)
    color_steps = list(map(expand_color, list(Color("blue").range_to(Color("red"), 65))))
    lcd.backlight = False
    for step in color_steps:
        lcd.clear()
        lcd.message = str(step)
        lcd.color = step
        sleep(0.1)
    for step in reversed(color_steps[:-1]):
        lcd.clear()
        lcd.message = str(step)
        lcd.color = step
        sleep(0.1)

    lcd.clear()

    lcd.message = f"Here are some\nspecial characters:\n{DEGREE_CHAR} {UP_ARROW_CHAR} {DOWN_ARROW_CHAR}"
    sleep(2)
    lcd.blacklight = False
    lcd.clear()
