## Dependencies 

```
sudo apt-get update
sudo pip install RPLCD
sudo apt-get install python3-gpiozero python3-rpi.gpio
```

# GAMEPLAY

<a href="http://www.youtube.com/watch?feature=player_embedded&v=G4lIUJDdov0" target="_blank"><img src="http://img.youtube.com/vi/G4lIUJDdov0/0.jpg" 
alt="" width="240" height="180" border="10" /></a> <--- press here

# HOW TO PLAY

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

