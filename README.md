## Used machine

Raspberry Pi 3 model B+

```uname -a```

Linux rpi 6.6.51+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.6.51-1+rpt3 (2024-10-08) aarch64 GNU/Linux


## Dependencies 

RPLCD, smbus2

My raspbian system already has all the necessary I2C and GPIO libraries, so if you have a different version of linux, 
google what extra you need to install.

```
python3 -m venv env
source env/bin/activate
pip install RPi.GPIO
pip install RPLCD
pip install smbus2
```

## Gameplay (from original author)

http://www.youtube.com/watch?feature=player_embedded&v=G4lIUJDdov0

## How to play

just use the buttons in the connection to move the stickman if you don't know what do the terminal will say what to do.

play with maximum contrast for a better experience


## GPIO Pins

### LCD

We use I2C interface.

- ...
- ...
- ...
- ...

### Buttons

4x4 matrix, but we use only 4 buttons.

I connected 8 pin to: gpio 16, 20, 21, 5, 6, 13, 19, 26

- S1 - UP: 
- S4 - RIGHT: 
- S13 - LEFT: 
- S16 - DOWN: 


## Solving problems

```
First it said command 'pip' not found, so I typed

sudo apt install python-pip

then it said

E: Unable to locate package python-pip
```

Identify the highest version of python listed. If the highest version is something like python2.7 then install 
python2-pip If its something like python3.8 then install python3-pip.

For example, if some guide says to install python-smbus, install python3-smbus.

---

```python3 -m pip install``

