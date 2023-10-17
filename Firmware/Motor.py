import gpiozero

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

    def __init__(self, forward, backward, speed):
        self.pin = forward
        self.speed = speed
        self.motor = gpiozero.Motor(forward=forward, backward=backward, pwm=True)

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