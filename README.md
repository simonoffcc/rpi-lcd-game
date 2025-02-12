## Configuration

Microcontroller: Raspberry Pi 3 model B+

System: Linux rpi 6.6.51+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.6.51-1+rpt3 (2024-10-08) aarch64 GNU/Linux


## Pinout

### LCD

I use I2C interface.

Scheme: RPi - I2C LCD Module
- 5V - VCC
- GND - GND
- Pin 3 (GPIO 2) - SDA
- Pin 5 (GPIO 3) - SLC

### Buttons

I use matrix keyboard 4x4 (16 buttons), but I use only 4 corner buttons for 4 actions.

I connected 8 pin to gpio: 
C4, C3, C2, C1, R1, R2, R3, R4 -> 16, 20, 21, 5, 6, 13, 19, 26

Scheme: Button on matrix (GPIO_Column, GPIO_Row) - action
- S1 (5, 6) - Move Up: 
- S4 (16, 6) - Move Right: 
- S13 (5, 26) - Move Left: 
- S16 (16, 26) - Move Down: 

The connected buttons that are empty for actions can be used to extend the functionality, 
for example, to pause the game.

If you lose, the script stops.


## Tuning

In the src/tests directory you can find scripts that will help you 
to test the correct connection of LCD display and matrix keyboard.



## Dependencies 

RPi.GPIO, RPLCD, smbus2

My raspbian system already has all the necessary I2C and GPIO libraries, so if you have a different version of linux, 
google what extra you need to install.

You should use virtual environment to prevent unforeseen errors.
```
python3 -m venv env
source env/bin/activate
```

Then just install dependencies:
```
pip install -r requirements.txt
```


## How to play

```
python src/game.py
```

Just use the corner buttons on the matrix to move the stickman. 
Adjust the contrast using a potentiometer (relevant for owners of I2C adapter for LCD).


## Demonstration

![Demonstration](https://github.com/simonoffcc/rpi-lcd-game/blob/master/images/demonstration.jpg)