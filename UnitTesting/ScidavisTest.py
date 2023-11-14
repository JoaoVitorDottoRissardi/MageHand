import gpiozero
from time import sleep

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

class Servo:

	def __init__(self, pin, angleStep, speed):
		self.pin = pin
		self.angleStep = angleStep
		self.speed = speed
		myCorrection=0.45
		maxPW=(2.0+myCorrection)/1000
		minPW=(1.0-myCorrection)/1000
		self.servo = gpiozero.AngularServo(pin=pin, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW)

	"""
        Function to spin the motor to a determined location

        Parameters
        ----------
        angle : int
             position to which the motor should spin to, in degrees. It must be a value between -90 and 90.
        
    """

	def spinTo(self, angle):
		currentAngle = self.servo.angle
		direction = currentAngle - angle
		print(angle)
		for i in range(int(currentAngle), angle, -1 if direction > 0 else 1):
			self.servo.angle = i
			sleep(1/self.speed)
		# self.servo.source_delay = (self.angleStep/self.speed)
		# self.servo.source = quantized([currentAngle/90, angle/90], deltaAngle/self.angleStep)

motor = Motor(14, 20, 1)

servo = Servo(3, 1, 30)

servo.spinTo(0) 

print("Initiating tests!!!")
input()

timeToPour = 3

tests = [1, 2, 3, 4, 5]

while timeToPour <= 10:
    for test in tests:
        motor.turnOn()
        sleep(timeToPour)
        motor.turnOff()
        print(f"Time: {timeToPour} ->  Sample {test}")
        servo.spinTo(-60) 
        for i in range(1, 31):
            servo.spinTo(-60 - i)
            sleep(1)
        input()
        servo.spinTo(0) 
        input()

    timeToPour += 0.5