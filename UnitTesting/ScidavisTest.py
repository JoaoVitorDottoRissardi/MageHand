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

	def __init__(self, pin, angleStep, speed, offset=0):
		self.pin = pin
		self.angleStep = angleStep
		self.speed = speed
		self.offset = offset
		myCorrection=0.45
		maxPW=(2.0+myCorrection)/1000
		minPW=(1.0-myCorrection)/1000
		self.min = max(-90-self.offset, -90)
		self.max = min(90-self.offset, 90)
		self.servo = gpiozero.AngularServo(pin=pin, min_angle=-90-self.offset, max_angle=90-self.offset, min_pulse_width=minPW, max_pulse_width=maxPW)
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
		# print(angle)
		for i in range(int(currentAngle), angle, -1 if direction > 0 else 1):
			self.servo.angle = (max(self.min, min(self.max, i)))
			sleep(1/self.speed)
	# def spinTo(self, angle):
	# 	# self.currentAngle = self.servo.angle
	# 	direction = self.currentAngle - (max(-90, min(90, angle+self.offset)))
	# 	print(self.currentAngle)
	# 	for i in range(int(self.currentAngle), (max(-90, min(90, angle+self.offset))), -1 if direction > 0 else 1):
	# 		self.servo.angle = max(-90, min(90, i+self.offset))
	# 		self.currentAngle = i+self.offset
	# 		sleep(1/self.speed)
		# self.servo.source_delay = (self.angleStep/self.speed)
		# self.servo.source = quantized([currentAngle/90, angle/90], deltaAngle/self.angleStep)

motor = Motor(23, 16, 1)
motor2 = Motor(14, 20, 1)

servo = Servo(2, 1, 30, 12)
servo2 = Servo(3, 1, 30)

# servo.spinTo(90)
# servo2.spinTo(-90)
# # sleep(2)
servo.spinTo(0)
servo2.spinTo(0)
# exit(0)

print("Initiating tests!!!")

# import av
# import numpy as np
# import time
# import pygame

# pygame.init()
# screen_width = 480
# screen_height = 320
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
# timestamp_ns = 0
# timestamp = 0

# container = av.open('/dev/video0')
# timestamp_ns = 0

# for frame in container.decode(video=0):
# 	frame = frame.to_ndarray(format=av.VideoFormat('rgb24'))
# 	# frame = np.rot90(frame)
# 	# frame = pygame.transform.scale(pygame.surfarray.make_surface(frame), (480,320))
# 	print(frame.shape)
# 	frame = pygame.surfarray.make_surface(frame)
# 	screen.blit(frame, (0, 0))
# 	pygame.display.flip()
# 	last_timestamp_ns = timestamp_ns
# 	timestamp_ns = time.monotonic_ns()
# 	print(f"Frame: fps {1000000000 / (timestamp_ns - last_timestamp_ns)}")


# import imageio.v3 as iio
# import numpy as np
# import time
# import pygame

# pygame.init()
# screen_width = 480
# screen_height = 320
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
# timestamp_ns = 0
# timestamp = 0

# # for idx, frame in enumerate(iio.imiter("/dev/video0", plugin='pyav')):
# for idx, frame in enumerate(iio.imiter("<video0>", fps=30, size=(640, 480), pixelformat='mjpeg')):
# 	# print(f"Frame {idx}: avg. color {np.sum(frame, axis=-1)}")
# 	frame = np.rot90(frame)
# 	frame = pygame.transform.scale(pygame.surfarray.make_surface(frame), (480,320))
# 	# frame = pygame.surfarray.make_surface(frame)
# 	screen.blit(frame, (0, 0))
# 	pygame.display.flip()
# 	last_timestamp_ns = timestamp_ns
# 	timestamp_ns = time.monotonic_ns()
# 	# ok = (1000000000 / (timestamp_ns - last_timestamp_ns)) < 24
# 	# while not ok:
# 	# 	timestamp_ns = time.monotonic_ns()
# 	# 	ok = (1000000000 / (timestamp_ns - last_timestamp_ns)) < 24
# 	print(f"Frame {idx}: fps {1000000000 / (timestamp_ns - last_timestamp_ns)}")

# exit(0)

# import numpy as np
# import cv2
# import time

# # gst_str = (
# #         "v4l2src device=/dev/video0 ! "
# #         "image/jpeg,width=(int)640,height=(int)480,framerate=30/1,"
# #         "format=(string)RGB ! "
# #         "jpegdec ! videoconvert ! appsink"
# #     )
#     # return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
# # capture = cv2.VideoCapture(0)
# gst_str = ' v4l2src device=/dev/video0 ! image/jpeg, format=MJPG ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'
# capture = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
# if not capture.isOpened():
# 	raise Exception('a')
# # W, H = 640, 480
# # # W, H = 1280, 720
# # capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
# # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
# # capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# # capture.set(cv2.CAP_PROP_FPS, 60)
# # capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# while True:
# 	ret, frame = capture.read()
# 	timestamp = capture.get(cv2.CAP_PROP_POS_MSEC)

# 	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# 	# frame = np.rot90(frame)
# 	# frame = pygame.transform.scale(pygame.surfarray.make_surface(frame), (480,320))
# 	frame = pygame.surfarray.make_surface(frame)
# 	screen.blit(frame, (0, 0))
# 	last_timestamp_ns = timestamp_ns
# 	last_timestamp = timestamp
# 	timestamp_ns = time.monotonic_ns()
# 	timestamp = timestamp_ns // 1000000
# 	pygame.display.flip()
# 	print(f"(fps={1000000000 / (timestamp_ns - last_timestamp_ns)})")

input()

timeToPour = 6.5

tests = [1, 2, 3]

while timeToPour <= 8:
	for test in tests:
		print(f"Time: {timeToPour} ->  Sample {test}")
		# motor.turnOn()
		# sleep(timeToPour)
		# motor.turnOff()
		# sleep(0.5)
		# servo.spinTo(45)
		# for i in range(1, 46):
		# 	servo.spinTo(45 + i)
		# 	sleep(0.03)
		# input()
		
		motor2.turnOn()
		sleep(timeToPour)
		motor2.turnOff()
		sleep(0.5)
		servo2.spinTo(-45)
		for i in range(1, 46):
			servo2.spinTo(-45 - i)
			sleep(0.03)
		input()
		servo.spinTo(0)
		servo2.spinTo(0)
		input()
		# motor.turnOn()
		# sleep(timeToPour)
		# motor.turnOff()
		# print(f"Time: {timeToPour} ->  Sample {test}")
		# sleep(1)
		# servo.spinTo(-45)
		# for i in range(1, 46):
		# 	servo.spinTo(-45 - i)
		# 	sleep(0.03)
		# input()
		# servo.spinTo(0)
		# input()
		# servo.spinTo(45) 
		# for i in range(1, 46):
		# 	servo.spinTo(45 + i)
		# 	sleep(0.03)
		# input()
		# servo.spinTo(0) 
		# input()

		# servo.spinTo(-45)
		# for i in range(1, 46):
		# 	servo.spinTo(-45 - i)
		# 	sleep(0.03)
		# input()
		# servo.spinTo(0) 
		# input()

	timeToPour += 0.5