import sys
from Display import Display
if "--test" in sys.argv:
    from Test.Motor import Motor
else:
    from Motor import Motor
if "--test" in sys.argv:
    from Test.Servo import Servo
else:
    from Servo import Servo
from time import sleep

"""
Class that represents the physical entity of the machine, it contains 2 motors, 2 servos and 1 display

Attributes
----------

display: Display
    Display class object, build based on displayParameters

servo1: Servo
    Servo class object, build based on servoParameters[1]

servo2: Servo
    Servo class object, build based on servoParameters[2]

motor1: Motor
    Motor class object, build based on motorParameters[1]

motor2: Servo
    Motor class object, build based on motorParameters[2]

Construcutor params
-------------------

displayParameters: dict
    dictionary containg the displayParameters. It must contain: colors, images, imageSize, imagePositions,
    textSize, textFont and borderWidth

servoParameters: dict
    dictionary containg the servoParameters. It must contain: 1 and 2. Each one is also a dict and should
    contain: pin, angleStep and speed.

motorParameters: dict
    dictionary containg the motorParameters. It must contain: 1 and 2. Each one is also a dict and should
    contain: pin and speed.

"""

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
            servoParameters['1']['pin'],
            servoParameters['1']['angleStep'],
            servoParameters['1']['speed']
        )

        self.servo2 = Servo(
            servoParameters['2']['pin'],
            servoParameters['2']['angleStep'],
            servoParameters['2']['speed']
        )

        self.motor1 = Motor(
            motorParameters['1']['forward'],
            motorParameters['1']['backward'],
            motorParameters['1']['speed']
        )

        self.motor2 = Motor(
            motorParameters['2']['forward'],
            motorParameters['2']['backward'],
            motorParameters['2']['speed']
        )

        # self.servo1 = None

        # self.servo2 = None

        # self.motor1 = None

        # self.motor2 = None

    """
        Function to move the cups to accept the candies

    """

    def acceptCandies(self):
        self.servo1.spinTo(90)
        self.servo2.spinTo(90)
        sleep(1)
        self.servo1.spinTo(0)
        self.servo2.spinTo(0)
    
    """
        Function to move the cups to reject the candies

    """

    def rejectCandies(self):
        self.servo1.spinTo(-90)
        self.servo2.spinTo(-90)
        sleep(1)
        self.servo1.spinTo(0)
        self.servo2.spinTo(0)

    """
        Function to move the cups to the idle position. Should be called only on boot

    """
    
    def resetCups(self):
        self.servo1.spinTo(0)
        self.servo2.spinTo(0)
    
    """
        Function to START pouring candy

        Parameters
        ----------

        candy: int
            what candy should START being poured into the cups. Either 1 or 2. 

    """
    
    def pourCandy(self, candy):
        if candy == 1:
            self.motor1.turnOn()
        else:
            self.motor2.turnOn()

    """
        Function to STOP pouring candy

        Parameters
        ----------

        candy: int
            what candy should STOP being poured into the cups. Either 1 or 2. 

    """

    def stopPouringCandy(self, candy):
        if candy == 1:
            self.motor1.turnOff()
        else:
            self.motor2.turnOff()

    """
        Function to show a message on the display that requests a gesture

        Parameters
        ----------

        message: str
            text that should be displayed. It must contain '\n' if line breaking is needed.
        
        type: str
            type of the content. For now, either 'Alert', 'Info' or 'Confirm'. This will
            automatically display the correspondent Icon image for this type.
        
        gestures: list[str]
            list of gestures' images that should be displayed along with the text.

    """

    def showGestureMessage(self, message, type, gestures):
        gestures.append(type)
        self.display.displayContent(type, message, gestures)


    """
        Function to show the message the customer should see while pouring candy

        Parameters
        ----------

        message: str
            text that should be displayed. It must contain '\n' if line breaking is needed.
        
        candies: list[str]
            what candies the customer currently have inside the cups. The options are
            either ['Candy1'], ['Candy2'] or ['Candy1','Candy2']

    """

    def showBuyingMessage(self, message, candies):
        candies.append('Info')
        self.display.displayContent('Info', message, candies)

    """
        Function to show the message the customer should see while selecting one type of candy

        Parameters
        ----------

        message: str
            text that should be displayed. It must contain '\n' if line breaking is needed.
        
        candy: str
            what candy the customer is currently selecting. The options are
            either 'Candy1' or 'Candy2'.

    """

    def showSelectionMessage(self, message, candy):     
        self.display.displayContent('Info', message, [candy, 'Info'])

    """
        Function to update the image of a certain candy

        Parameters
        ----------

        candy: str
            what candy should be update. The options are either 'Candy1' or 'Candy2'.

    """

    def updateCandyImage(self, candy):
        self.display.updateImage(candy)

# print("Oi")

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
#         'pin': 2,
#         'angleStep': 1,
#         'speed': 90
#     },
#     2:{
#         'pin': 3,
#         'angleStep': 1,
#         'speed': 90
#     }
# }

# motorParameters = {
#     1:{
#         'forward': 23,
#         'backward': 16,
#         'speed': 0.5
#     },
#     2:{
#         'forward': 24,
#         'backward': 20,
#         'speed': 0.5
#     }
# }

# print("init creation")

# machine = Machine(displayParameters, servoParameters, motorParameters)

# while True:

#     print("init loop")

#     machine.showGestureMessage('teste', 'Alert', ['Peace', 'Stop', 'ThumbsUp'])

#     sleep(5)

#     # machine.showGestureMessage('teste', 'Info', ['Stop'])

#     # sleep(5)

#     # machine.showGestureMessage('teste', 'Confirm', ['ThumbsUp'])

#     # sleep(5)

#     # machine.showGestureMessage('teste', 'Alert', ['ThumbsDown'])

#     # sleep(5)

#     # machine.showGestureMessage('teste', 'Info', ['Fist'])

#     # sleep(5)

#     machine.showBuyingMessage('teste', ['Candy1', 'Candy2'])

#     sleep(5)

#     print("Aceitar doces")

#     machine.acceptCandies()

#     sleep(5)

#     print("Rejeitar doces")

#     machine.rejectCandies()

#     sleep(5)

#     # print("Colocar doce 1")

#     # machine.pourCandy(1)

#     # sleep(5)

#     # print("Colocar doce 2")

#     # machine.stopPouringCandy(1)

#     # machine.pourCandy(2)

#     # sleep(5)

#     # machine.stopPouringCandy(2)
