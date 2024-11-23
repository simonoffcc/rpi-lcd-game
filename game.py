# import time
# import warnings
# import random
# import RPi.GPIO as GPIO
# from RPLCD.i2c import CharLCD
#
# # Initialize LCD
# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
#               cols=16, rows=2, dotsize=8,
#               charmap='A02',
#               auto_linebreaks=True,
#               backlight_enabled=True)
# lcd.clear()
#
# warnings.simplefilter("ignore")
#
# # Custom characters
# line = (
#     0b00000,
#     0b00000,
#     0b00000,
#     0b11111,
#     0b00000,
#     0b00000,
#     0b00000,
#     0b00000
# )
# stickman = (
#     0b00100,
#     0b01010,
#     0b00100,
#     0b01110,
#     0b10101,
#     0b00100,
#     0b01010,
#     0b10001
# )
# lcd.create_char(1, stickman)
# lcd.create_char(2, line)
#
# # Keypad setup
# KEYPAD = [
#     ["up", 0, 0, "right"],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     ["left", 0, 0, "down"]
# ]
#
# ROWS = [6, 13, 19, 26]
# COLS = [5, 21, 20, 16]
#
# GPIO.setmode(GPIO.BCM)
#
# for row_pin in ROWS:
#     GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
# for col_pin in COLS:
#     GPIO.setup(col_pin, GPIO.OUT)
#     GPIO.output(col_pin, GPIO.HIGH)
#
#
# def get_key():
#     key = None
#     for col_num, col_pin in enumerate(COLS):
#         GPIO.output(col_pin, GPIO.LOW)
#         for row_num, row_pin in enumerate(ROWS):
#             if GPIO.input(row_pin) == GPIO.LOW:
#                 key = KEYPAD[row_num][col_num]
#                 while GPIO.input(row_pin) == GPIO.LOW:
#                     time.sleep(0.05)
#         GPIO.output(col_pin, GPIO.HIGH)
#     return key
#
#
# class Player:
#     x = 0
#     y = 0
#
#     def __init__(self):
#         self.update()
#
#     def update(self):
#         lcd.cursor_pos = (self.y, self.x)
#         lcd.write_string(chr(1))
#         lcd.cursor_pos = (self.y, self.x)
#
#     def move(self, dir):
#         if dir == "up" and self.y == 1:
#             lcd.cursor_pos = (self.y, self.x)
#             lcd.write_string(" ")
#             self.y -= 1
#         elif dir == "down" and self.y == 0:
#             lcd.cursor_pos = (self.y, self.x)
#             lcd.write_string(" ")
#             self.y += 1
#         elif dir == "left" and 1 <= self.x <= 15:
#             lcd.cursor_pos = (self.y, self.x)
#             lcd.write_string(" ")
#             self.x -= 1
#         elif dir == "right" and 0 <= self.x < 14:
#             lcd.cursor_pos = (self.y, self.x)
#             lcd.write_string(" ")
#             self.x += 1
#         self.update()  # Ensure the player is updated after moving
#
#
# class Enemy:
#     x = 15
#     y = 0
#
#     def __init__(self, x=None, y=None):
#         if x is None and y is None:
#             self.x = 15
#             self.y = random.randint(0, 1)
#         else:
#             self.x = x
#             self.y = y
#
#     def update(self):
#         lcd.cursor_pos = (self.y, self.x)
#         lcd.write_string(chr(2))
#
#     def move(self, dir):
#         if dir == "left" and 1 <= self.x <= 15:
#             lcd.cursor_pos = (self.y, self.x)
#             lcd.write_string(" ")
#             self.x -= 1
#             self.update()
#
#
# def init():
#     lcd.cursor_mode = "hide"
#
#
# player = Player()
#
# enemies = []
# score = 0
# Game = True
#
#
# def logic():
#     global Game, score
#     if random.random() < 0.5:  # vary to make harder?
#         if len(enemies) > 0:
#             X = enemies[-1].x
#             Y = enemies[-1].y
#             if X == 14:
#                 enemies.append(Enemy(X + 1, Y))
#             else:
#                 enemies.append(Enemy())
#         else:
#             enemies.append(Enemy())
#
#     for e in enemies[::-1]:
#         e.move("left")
#         if e.x == 0:
#             enemies.remove(e)
#             score += 1
#         if e.x == player.x and e.y == player.y:
#             Game = False
#
#
# def collision():
#     for e in enemies[::-1]:
#         if e.x == player.x and e.y == player.y:
#             Game = False
#
#
# def main_loop():
#     global Game, score
#     speed = 0.5
#     gg = 1
#     while Game:
#         if gg % 20 == 0 and round(speed, 2) > 0.05:
#             speed -= 0.05
#         lcd.clear()
#         logic()
#         for e in enemies[::-1]:
#             e.update()
#         collision()
#         player.update()
#         time.sleep(round(speed, 2))
#         gg += 1
#
#
# def main():
#     global Game, score, enemies
#     init()
#     while True:
#         if Game:
#             main_loop()
#         else:
#             lcd.clear()
#             lcd.write_string(f"   Game Over !\n\rScore: {score}")
#             time.sleep(3)
#             lcd.clear()
#             lcd.write_string("Play Again?\n\r+ YES    + NO")
#             lcd.cursor_mode = "line"
#             Yes()
#             while True:
#                 key = get_key()
#                 if key == "left":
#                     lcd.cursor_pos = (1, 0)
#                 elif key == "right":
#                     lcd.cursor_pos = (1, 9)
#                 elif key in ["up", "down"]:
#                     if lcd.cursor_pos == (1, 0):
#                         player.x = 0
#                         player.y = 0
#                         enemies = []
#                         score = 0
#                         Game = True
#                         break
#                     elif lcd.cursor_pos == (1, 9):
#                         lcd.cursor_mode = "hide"
#                         lcd.clear()
#                         lcd.close()
#                         GPIO.cleanup()
#                         exit()
#                 time.sleep(0.1)
#
#
# try:
#     main()
# except KeyboardInterrupt:
#     lcd.clear()
#     lcd.close(clear=True)
#     GPIO.cleanup()
