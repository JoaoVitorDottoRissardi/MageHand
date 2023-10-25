"""
Dummy Class for testing logic

Attributes
----------

pin: int
    in which pin of the raspberry the motor transistor will be connected.
    This pin follows the BCM pattern. Therefore, it is always the GPIO number, 
    not the raspberry pin number.

speed: int
    speed of the motor. Value between 0 and 1. 0 is no speed while 1 is full speed.

motor: Motor
    gpiozero class that represents a Motor.

"""

class Motor:

    def __init__(self, forward, backward, speed):
        self.pin = forward
        self.speed = speed

    """
        Function to turn ON the motor

    """

    def turnOn(self):
        print("DC Motor is turned on")

    """
        Function to turn OFF the motor

    """

    def turnOff(self):
        print("DC motor is turned off")
