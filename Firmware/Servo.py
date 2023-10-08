from gpiozero import AngularServo 
from gpiozero.tools import quantized

"""
Class for handling the Servo motor functions

Attributes
----------

pin: int
    in which pin of the raspberry the motor transistor will be connected.
    This pin follows the BCM pattern. Therefore, it is always the GPIO number, 
    not the raspberry pin number.

angleStep: float
	the step with which the motor should spin, in degrees.

speed: float
    speed of the motor, in degrees per second.

servo: Servo
	gpiozero class that represents a Servo

"""

class Servo:

	def __init__(self, pin, angleStep, speed):
		self.pin = pin
		self.angleStep = angleStep
		self.speed = speed
		# myCorrection=0.45
		# maxPW=(2.0+myCorrection)/1000
		# minPW=(1.0-myCorrection)/1000
		self.servo = AngularServo(pin=pin, min_angle=-90, max_angle=90)

	"""
        Function to spin the motor to a determined location

        Parameters
        ----------
        angle : int
             position to which the motor should spin to, in degrees. It must be a value between -90 and 90.
        
    """

	def spinTo(self, angle):
		currentAngle = self.servo.angle
		deltaAngle = currentAngle - angle
		print('current angle: ', currentAngle)
		self.servo.source = quantized([currentAngle, angle], deltaAngle/self.angleStep)
		self.servo.source_delay = (self.angleStep/self.speed)

