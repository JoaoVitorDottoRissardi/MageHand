from gpiozero import Motor

class Motor:

    def __init__(self, pin, speed):
        self.pin = pin
        self.speed = speed
        self.motor = Motor(pin=pin, pwm=True)
    
    def turnOn(self):
        self.motor.forward(self.speed)
    
    def turnOff(self):
        self.motor.stop() 