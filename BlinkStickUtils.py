from blinkstick.blinkstick import BlinkStick
from blinkstick import blinkstick

def find_all_blinksticks():
    return blinkstick.find_all()

def blink(stick: BlinkStick):
    # Implementation of blink() is up to you.
    print("Blink called!")
    stick.pulse(red=255, duration=1000, repeats=5)