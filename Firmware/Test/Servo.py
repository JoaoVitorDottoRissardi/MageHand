from time import sleep

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
		# self.servo = AngularServo(pin=pin, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW)

	"""
        Function to spin the motor to a determined location

        Parameters
        ----------
        angle : int
             position to which the motor should spin to, in degrees. It must be a value between -90 and 90.
        
    """

	def spinTo(self, angle):
		print(f"Servo is spinning to {angle} degrees")
		# self.servo.source_delay = (self.angleStep/self.speed)
		# self.servo.source = quantized([currentAngle/90, angle/90], deltaAngle/self.angleStep)
		
# servo = Servo(25, 1, 90)

# sleep(2)

# servo.spinTo(90)


# while True:
# 	pass

