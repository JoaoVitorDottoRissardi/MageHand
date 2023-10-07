from Display import Display
from Motor import Motor
from Servo import Servo

from time import sleep

class Machine:

    def __init__(self, displayParameters, servoParameters, motorParameters):

        self.display = Display(
            displayParameters['colors'], 
            displayParameters['images'],
            displayParameters['imageSize'],
            displayParameters['imagePositions'],
            displayParameters['textSize'],
            displayParameters['textFont'],
            displayParameters['borderWidth']
        )

        self.servo1 = Servo(
            servoParameters[1]['pin'],
            servoParameters[1]['angleStep'],
            servoParameters[1]['speed']
        )

        self.servo2 = Servo(
            servoParameters[2]['pin'],
            servoParameters[2]['angleStep'],
            servoParameters[2]['speed']
        )

        self.motor1 = Motor(
            motorParameters[1]['pin'],
            motorParameters[1]['speed']
        )

        self.motor2 = Motor(
            motorParameters[2]['pin'],
            motorParameters[2]['speed']
        )

        # self.servo1 = None

        # self.servo2 = None

        # self.motor1 = None

        # self.motor2 = None

    def acceptCandies(self):
        self.servo1.spinTo(90)
        self.servo2.spinTo(90)
        self.servo1.spinTo(0)
        self.servo2.spinTo(0)

    def rejectCandies(self):
        self.servo1.spinTo(-90)
        self.servo2.spinTo(-90)
        self.servo1.spinTo(0)
        self.servo2.spinTo(0)
    
    def resetCups(self):
        self.servo1.spinTo(0)
        self.servo2.spinTo(0)
    
    def pourCandy(self, candy):
        if candy == 1:
            self.motor1.turnOn()
        else:
            self.motor2.turnOn()

    def stopPouringCandy(self, candy):
        if candy == 1:
            self.motor1.turnOff()
        else:
            self.motor2.turnOff()

    def showGestureMessage(self, message, type, gestures):
        gestures.append(type)
        self.display.displayContent(type, message, gestures)

    def showBuyingMessage(self, message, candies):
        candies.append('Info')
        self.display.displayContent('Info', message, candies)

    def showSelectionMessage(self, message, candy):     
        self.display.displayContent('Info', message, [candy, 'Info'])

    def updateCandyImage(self, candy):
        self.display.updateImage(candy)

# displayParameters = {
# 	'colors' : {
# 		'Alert' : (255,0,0),
# 		'Info' : (0,0,255),
# 		'Confirm' : (0,255,0),
# 		'Text' : (0,0,0),
# 		'Background' : (255,255,255)
# 	},
# 	'imageSize' : 75,
# 	'imagePositions' : {
# 		'Icon' : (30,30),
# 		'Candy' : (375, 30),
# 		'Gesture' : (375, 215)
# 	},
# 	'textSize' : 45,
# 	'textFont' : None,
# 	'borderWidth' : 20,
# 	'images' : {
# 		'Info' : {
# 			'type' : 'Icon',
# 			'path' : './images/info.png'
# 		},
# 		'Alert' : {
# 			'type' : 'Icon',
# 			'path' : './images/alert.png'
# 		},
# 		'Confirm' : {
# 			'type' : 'Icon',
# 			'path' : './images/confirm.jpg'
# 		},
# 		'ThumbsUp' : {
# 			'type' : 'Gesture',
# 			'path' : './images/thumbs_up.png'
# 		},
#         'ThumbsDown' : {
# 			'type' : 'Gesture',
# 			'path' : './images/thumbs_down.png'
# 		},
#         'Stop' : {
# 			'type' : 'Gesture',
# 			'path' : './images/stop.png'
# 		},
#         'Fist' : {
# 			'type' : 'Gesture',
# 			'path' : './images/fist.png'
# 		},
#         'Peace' : {
# 			'type' : 'Gesture',
# 			'path' : './images/peace.png'
# 		},
#         'Candy1' : {
#             'type' : 'Candy',
#             'path' : './images/mms.jpg'
#         },
#         'Candy2' : {
#             'type' : 'Candy',
#             'path' : './images/jelly_beans.jpg'
#         }
# 	}

# }

# servoParameters = {
#     1:{
#         'pin': 1,
#         'angleStep': 1,
#         'speed': 1
#     },
#     2:{
#         'pin': 1,
#         'angleStep': 1,
#         'speed': 1
#     }
# }

# motorParameters = {
#     1:{
#         'pin': 1,
#         'speed': 1
#     },
#     2:{
#         'pin': 1,
#         'speed': 1
#     }
# }

# machine = Machine(displayParameters, servoParameters, motorParameters)

# machine.showGestureMessage('teste', 'Alert', ['Peace', 'Stop', 'ThumbsUp'])

# sleep(5)

# # machine.showGestureMessage('teste', 'Info', ['Stop'])

# # sleep(5)

# # machine.showGestureMessage('teste', 'Confirm', ['ThumbsUp'])

# # sleep(5)

# # machine.showGestureMessage('teste', 'Alert', ['ThumbsDown'])

# # sleep(5)

# # machine.showGestureMessage('teste', 'Info', ['Fist'])

# # sleep(5)

# machine.showBuyingMessage('teste', ['Candy1', 'Candy2'])

# sleep(5)
