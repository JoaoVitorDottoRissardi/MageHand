from gpiozero import Motor

"""
Class for handling the DC motor functions

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

    def __init__(self, pin, speed):
        self.pin = pin
        self.speed = speed
        self.motor = Motor(pin=pin, pwm=True)

    """
        Function to turn ON the motor

    """

    def turnOn(self):
        self.motor.forward(self.speed)
    
    """
        Function to turn OFF the motor

    """

    def turnOff(self):
        self.motor.stop() 