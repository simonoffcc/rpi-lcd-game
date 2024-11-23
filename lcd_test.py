from RPLCD.i2c import CharLCD
from time import sleep


# lcd = CharLCD('PCF8574', 0x27)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

if __name__ == '__main__':
    print("start")
    lcd.clear()
    lcd.write_string('Hello world')
    sleep(3)
    print("hello world 1")
    lcd.clear()
    lcd.write_string('Hello\nWorld!')
    sleep(3)
    print("hello world 2")
    lcd.clear()
