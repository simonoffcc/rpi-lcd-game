import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Настройка матричной клавиатуры
KEYPAD = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
    [None, "interrupt", None, None]
]

ROWS = [6, 13, 19, 26]
COLS = [5, 21, 20, 16]

GPIO.setmode(GPIO.BCM)

for row_pin in ROWS:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for col_pin in COLS:
    GPIO.setup(col_pin, GPIO.OUT)
    GPIO.output(col_pin, GPIO.HIGH)

def get_key():
    key = None
    for col_num, col_pin in enumerate(COLS):
        GPIO.output(col_pin, GPIO.LOW)
        for row_num, row_pin in enumerate(ROWS):
            if GPIO.input(row_pin) == GPIO.LOW:
                key = KEYPAD[row_num][col_num]
                while GPIO.input(row_pin) == GPIO.LOW:
                    time.sleep(0.02)
        GPIO.output(col_pin, GPIO.HIGH)
    return key

def main():
    pause_state = False
    with open('/tmp/game_interrupt', 'w') as f:
        f.write('run')

    while True:
        key = get_key()
        if key == 'interrupt':
            pause_state = not pause_state
            with open('/tmp/game_interrupt', 'w') as f:
                if pause_state:
                    f.write('interrupt')
                else:
                    f.write('run')
        time.sleep(0.1)

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
