import time
import random
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

GPIO.setwarnings(False)

# Настройка LCD экрана
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
lcd.clear()

# Определение персонажей и препятствий
stickman = (
    0b00100,
    0b01010,
    0b00100,
    0b01110,
    0b10101,
    0b00100,
    0b01010,
    0b10001
)
obstacle = (
    0b00000,
    0b00000,
    0b11111,
    0b11111,
    0b11111,
    0b00000,
    0b00000,
    0b00000
)

lcd.create_char(1, stickman)
lcd.create_char(2, obstacle)

# Настройка матричной клавиатуры
KEYPAD = [
    ["up", None, None, "right"],
    [None, None, "pause", None],
    [None, None, None, None],
    ["left", None, None, "down"]
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
                    time.sleep(0.05)
        GPIO.output(col_pin, GPIO.HIGH)
    return key

# Класс игрока
class Player:
    def __init__(self):
        self.x = 0
        self.y = 1
        self.update()

    def update(self):
        lcd.cursor_pos = (self.y, self.x)
        lcd.write_string(chr(1))

    def move(self, direction):
        lcd.cursor_pos = (self.y, self.x)
        lcd.write_string(' ')
        if direction == 'up' and self.y > 0:
            self.y -= 1
        elif direction == 'down' and self.y < 1:
            self.y += 1
        elif direction == 'left' and self.x > 0:
            self.x -= 1
        elif direction == 'right' and self.x < 12:
            self.x += 1
        self.update()

# Класс препятствия
class Obstacle:
    def __init__(self, x=12):
        self.x = x
        self.y = random.randint(0, 1)

    def update(self):
        lcd.cursor_pos = (self.y, self.x)
        lcd.write_string(chr(2))

    def move(self):
        lcd.cursor_pos = (self.y, self.x)
        lcd.write_string(' ')
        self.x -= 1
        self.update()

# Основной игровой цикл
def game(best_score):
    player = Player()
    obstacles = []
    game_over = False
    score = 0
    speed = 0.7
    last_obstacle_x = 12
    paused = False

    while not game_over:
        key = get_key()
        if key:
            if key == 'pause':
                paused = not paused
                if paused:
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string('Paused')
                else:
                    lcd.clear()
                    player.update()
                    for obstacle in obstacles:
                        obstacle.update()
                    lcd.cursor_pos = (0, 13)
                    lcd.write_string(f'{score:03}')
                    lcd.cursor_pos = (1, 13)
                    lcd.write_string(f'{best_score:03}')
                continue
            if not paused:
                player.move(key)

        if not paused:
            # Добавление новых препятствий с проверкой расстояния
            if random.random() < 0.1 and (len(obstacles) == 0 or last_obstacle_x - obstacles[-1].x >= 3):
                new_obstacle = Obstacle()
                obstacles.append(new_obstacle)
                last_obstacle_x = new_obstacle.x

            # Обновление состояния препятствий
            for obstacle in obstacles:
                obstacle.move()
                if obstacle.x == 0:
                    obstacles.remove(obstacle)
                    score += 1
                if obstacle.x == player.x and obstacle.y == player.y:
                    game_over = True

            time.sleep(speed)
            lcd.clear()
            # Обновление счета на экране
            lcd.cursor_pos = (0, 13)
            lcd.write_string(f'{score:03}')
            lcd.cursor_pos = (1, 13)
            lcd.write_string(f'{best_score:03}')
            player.update()
            for obstacle in obstacles:
                obstacle.update()

    lcd.clear()
    if score > best_score:
        best_score = score
        lcd.write_string(f'New Record!\r\nScore: {score}')
    else:
        lcd.write_string(f'Game Over!\r\nScore: {score}')
    time.sleep(3)
    return best_score

def main():
    best_score = 0
    while True:
        best_score = game(best_score)
        lcd.clear()
        lcd.write_string('Press any key\r\nto restart')
        while not get_key():
            time.sleep(0.1)
        lcd.clear()

try:
    main()
except KeyboardInterrupt:
    lcd.clear()
    lcd.close(clear=True)
    GPIO.cleanup()
