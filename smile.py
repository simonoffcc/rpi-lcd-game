import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

GPIO.setwarnings(False)

# Инициализация дисплея
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
lcd.clear()

# Определение пользовательского символа смайлика
smiley = (
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b10001,
    0b01110,
    0b00000,
    0b00000
)

lcd.create_char(0, smiley)

# Вывод смайлика на экран
lcd.cursor_pos = (0, 0)
lcd.write_string(chr(0))

# Ожидание 3 секунды перед очисткой экрана
time.sleep(3)
lcd.clear()
