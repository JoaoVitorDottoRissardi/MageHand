from gpiozero import AngularServo 
from gpiozero.tools import quantized
from time import sleep	

class Servo:

	def __init__(self, pin, angleStep, speed):
		self.pin = pin
		self.angleStep = angleStep
		self.speed = speed
		# myCorrection=0.45
		# maxPW=(2.0+myCorrection)/1000
		# minPW=(1.0-myCorrection)/1000
		self.servo = AngularServo(pin=pin, min_angle=-90, max_angle=90)

	def spinTo(self, angle):
		currentAngle = self.servo.angle
		deltaAngle = currentAngle - angle
		print('current angle: ', currentAngle)
		self.servo.source = quantized([currentAngle, angle], deltaAngle/self.angleStep)
		self.servo.source_delay = (self.angleStep/self.speed)

