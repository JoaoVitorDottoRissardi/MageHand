import sys
from PaymentManager import PaymentManager
from Machine import Machine
if "--test" in sys.argv:
    from Test.GestureRecognizer import GestureRecognizer
else:
    from GestureRecognizer import GestureRecognizer
from pathlib import Path # needs python 3.4
import json
import requests
import threading
import datetime
import sseclient # sseclient-py
from dataclasses import dataclass # needs python 3.7
from time import sleep

"""
Struct to represent the candies in the machine compatible with firebase updates
(dataclasses need python 3.7, if fail change for dict)

Attributes
----------

name: String
    Candy name to be displayed

price: float
    price per mililiter of candy

volume: float
    currently available candy volume

image: Path
    path to image of candy
"""
@dataclass
class Candy:
    name: str
    price: float
    volume: float
    image: Path


"""
Class that represents the state machine of the structure and is the top-level entity of the project.

Attributes
----------

machine: Machine
    Machine class object, build based on the configuration found at ~/.config/MageHand/MageHandParameters.json

gestureRecognizer: GestureRecognizer
    GestureRecognizer class object

paymentManager: PaymentManager
    PaymentManager class object

dataDir: Path
    path to /var/lib/MageHand, which should be used for state information according to FHS

stateFile: Path
    path to text file used to log current phase in order to aid in crash recovery

phases: dict
    dictionary containing a mapping of strings to phase functions, so that phase transistions are not nested calls (see end of file)

"""
import socket
def is_connected():
  try:
    # See if we can resolve the host name - tells us if there is
    # A DNS listening
    # Connect to the host - tells us if the host is actually reachable
    s = socket.create_connection(("one.one.one.one", 80), 2)
    s.close()
    return True
  except Exception:
     pass # We ignore any errors, returning False
  return False

class MageHand:
    functions_url = "https://us-central1-mage-hand-demo.cloudfunctions.net"
    firebase_url = "https://mage-hand-demo-default-rtdb.firebaseio.com/"
    candy_1_storage_url = "https://firebasestorage.googleapis.com/v0/b/mage-hand-demo.appspot.com/o/kJyBx6wkKxblBQZn1Xc1BDLikH93%2FCandy1.jpg?alt=media"
    candy_2_storage_url = "https://firebasestorage.googleapis.com/v0/b/mage-hand-demo.appspot.com/o/kJyBx6wkKxblBQZn1Xc1BDLikH93%2FCandy2.jpg?alt=media"
    minVolume = 10
    maxCupVolume = 200
    volumePerSecond = 30
    name_conversion = {
        "ThumbsUp": "Thumbs Up",
        "ThumbsDown": "Thumbs Down",
        "Peace": "Peace",
        "Fist": "Fist",
        "Stop": "Stop"
    }
    action_conversion = {
        "ThumbsUp": "accept the order",
        "ThumbsDown": "reject the order",
        "Peace": "buy more candy",
        "Fist": "",
        "Stop": ""
    }
    def __init__(self):
        self.user = "kJyBx6wkKxblBQZn1Xc1BDLikH93"
        config = (Path.home() / ".config/MageHand/MageHandParameters.json").read_text()
        params = json.loads(config)

        self.machine = Machine(params["displayParameters"], params["servoParameters"], params["motorParameters"])
        self.machine.showGestureMessage('Initializing MageHand', 'Info', ["Peace"])

        self.gestureRecognizer = GestureRecognizer()
        self.paymentManager = PaymentManager()


        self.sync = threading.Event()
        self.firebaseThread = threading.Thread(target=self.firebaseCallbackFunction, daemon=True)

        self.dataDir = Path("/var/lib/MageHand")
        self.dataDir.mkdir(exist_ok=True)

        self.storage1 = self.dataDir / "storage1.txt"
        self.storage2 = self.dataDir / "storage2.txt"

        self.cupFile1 = self.dataDir / "cupFile1.txt"
        self.cupFile2 = self.dataDir / "cupFile2.txt"

        if not self.storage1.exists():
            self.storage1.write_text("{:.2f}".format(0.0))

        if not self.storage2.exists():
            self.storage2.write_text("{:.2f}".format(0.0))

        if not self.cupFile1.exists():
            self.cupFile1.write_text("{:.2f}".format(0.0))

        if not self.cupFile2.exists():
            self.cupFile2.write_text("{:.2f}".format(0.0))

        if (self.dataDir / "candyInformation.json").exists():
            candyFile = (self.dataDir / "candyInformation.json").read_text()
            candyData = json.loads(candyFile)
            c1 = candyData["Candy1"]
            c2 = candyData["Candy2"]
            self.candy1 = Candy(c1["Name"], float(c1["Price"]), float(self.storage1.read_text()), 'images/candy1.png')
            self.candy2 = Candy(c2["Name"], float(c2["Price"]), float(self.storage2.read_text()), 'images/candy2.png')
        else:
            self.getFirebaseCandyInformation()

        self.machine.updateCandyImage('Candy1')
        self.machine.updateCandyImage('Candy2')

        self.selectedCandy = None
        self.stateFile = self.dataDir / "current_state.txt"
        self.cupVolume1 = [float(self.cupFile1.read_text())]
        self.cupVolume2 = [float(self.cupFile2.read_text())]
        self.cupPrice1 = [0]
        self.cupPrice2 = [0]

        self.phases = {
            "boot": self.bootPhaseFunction,
            "introduction": self.introductionPhaseFunction,
            "confirmation": self.confirmationPhaseFunction,
            "selection": self.selectionPhaseFunction,
            "pouring": self.pouringPhaseFunction,
            "decision": self.decisionPhaseFunction,
            "payment": self.paymentPhaseFunction
        }

    def rejectCandies(self, reason):
        self.machine.rejectCandies()
        date = datetime.datetime.now()
        index = requests.get(MageHand.firebase_url + self.user + "/OrderHistory/OrderCount.json").json()
        histDict = { f"{date.date().isoformat()}/{date.time().isoformat('seconds')}": {
            "Candy1Name": self.candy1.name,
            "Candy2Name": self.candy2.name,
            "Price1": self.cupPrice1[0],
            "Price2": self.cupPrice2[0],
            "Quantity1": self.cupVolume1[0],
            "Quantity2": self.cupVolume2[0],
            "Total": (self.cupPrice1[0] + self.cupPrice2[0]),
            "AdditionalInfo": reason,
            "Status": "Rejected",
            "Index": index+1
        },
         "OrderCount": index+1           }
        response = requests.patch(MageHand.firebase_url + self.user + "/OrderHistory.json", data=json.dumps(histDict))
        response2 = requests.patch(MageHand.firebase_url + self.user + "/candyInformation.json", data=json.dumps({ "Candy1/Volume": self.candy1.volume, "Candy2/Volume": self.candy2.volume }))


    def acceptCandies(self, reason):
        self.machine.acceptCandies()
        date = datetime.datetime.now()
        index = requests.get(MageHand.firebase_url + self.user + "/OrderHistory/OrderCount.json").json()
        histDict = { f"{date.date().isoformat()}/{date.time().isoformat('seconds')}": {
            "Candy1Name": self.candy1.name,
            "Candy2Name": self.candy2.name,
            "Price1": self.cupPrice1[0],
            "Price2": self.cupPrice2[0],
            "Quantity1": self.cupVolume1[0],
            "Quantity2": self.cupVolume2[0],
            "Total": (self.cupPrice1[0] + self.cupPrice2[0]),
            "AdditionalInfo": reason,
            "Status": "Successful",
            "Index": index+1
        },
         "OrderCount": index+1           }
        response = requests.patch(MageHand.firebase_url + self.user + "/OrderHistory.json", data=json.dumps(histDict))
        response2 = requests.patch(MageHand.firebase_url + self.user + "/candyInformation.json", data=json.dumps({ "Candy1/Volume": self.candy1.volume, "Candy2/Volume": self.candy2.volume }))

    """
        Function to initiate the boot phase
    """
    def bootPhaseFunction(self):
        lastPhase = self.stateFile.read_text() if self.stateFile.exists() else ""

        self.syncFirebase(ignore=True)
        self.machine.showGestureMessage('Initializing MageHand', 'Info', ["Peace"])
        self.firebaseThread.start()

        if lastPhase == "payment":
            self.machine.acceptCandies()
        else:
            self.rejectCandies("System was not in payment during last shutdown")

        return "introduction"


    """
        Function to initiate the introduction phase
    """
    def introductionPhaseFunction(self):
        self.stateFile.write_text("introduction")
        self.cupVolume1 = [0]
        self.cupVolume2 = [0]
        self.cupPrice1 = [0]
        self.cupPrice2 = [0]

        while not is_connected():
            self.machine.showGestureMessage("No Internet Connection \n Please Wait", "Alert", [])
            sleep(1)

        self.syncFirebase(ignore=True)

        if not self.paymentManager.hasPaymentKeys():
            self.machine.showGestureMessage('There are no payment keys configured \n Cannot proceed', 'Alert', [])
        
        self.getFirebasePaymentKeys()

        self.machine.showGestureMessage('Make a Stop sign to proceed', 'Info', ['Stop'])
        sleep(4)

        def none_callback(frame, **kargs):
            import numpy as np
            frame = np.rot90(frame)
            self.machine.showImage(frame)
            return 'introduction'
            
        def undefined_callback(**kargs):
            # self.machine.showGestureMessage('Hand detected \n Do a Stop sign to proceed', 'Info', ['Stop'])
            self.machine.showScreen('tela001.png')
            return 'introduction'
        
        def stop_callback(**kargs):
            self.machine.showGestureMessage('Confirm the Stop sign\nfor 4 seconds to proceed', 'Confirm', ['Stop'])
            return 'introduction'
        
        return self.gestureRecognizer.runState(
            "introduction",
            ["Stop", "None", "Undefined"],
            {
                "Stop": stop_callback,
                "None": none_callback,
                "Undefined": undefined_callback
            },
            ["Stop"],
            {
                "Stop": lambda **kargs: "confirmation"
            }
        )


    """
        Function to initiate the confirmation phase
    """
    def confirmationPhaseFunction(self):
        self.stateFile.write_text("confirmation")
        
        def undefined_callback(**kargs):
            self.machine.showGestureMessage('Customer Detected \n Do a Thumbs Up to Buy Candy', 'Info', ["ThumbsUp"])
            return "confirmation"
        
        def none_callback(**kargs):
            self.machine.showGestureMessage("Lost track of hand \n Show a Thumbs Up to Select Candy", "Alert", ["ThumbsUp"])
            return "confirmation"

        self.machine.showGestureMessage('Customer Detected \n Do a Thumbs Up to Buy Candy', 'Info', ["ThumbsUp"])
        return self.gestureRecognizer.runState("confirmation", ["ThumbsUp", "None", "Undefined"], {"Undefined": undefined_callback, "None": none_callback, "ThumbsUp": lambda **kargs: "selection"}
                                        , ["None"],{"None": lambda **kargs: "introduction"})

    """
        Function to initiate the selection phase
    """
    def selectionPhaseFunction(self):
        self.stateFile.write_text("selection")
        self.machine.showGestureMessage('Do a Stop gesture to \n start selecting candies', 'Info', ["Stop"])
        sleep(3)

        def undefined_callback(Xpositions, **kargs):
            mean = sum(Xpositions) / len(Xpositions)
            # print(f"Posicao detectada = {mean}")

            self.selectedCandy = 1 if mean < 0.5 else 2
            c = self.candy1 if self.selectedCandy == 1 else self.candy2
            cupPrice = self.cupPrice1 if self.selectedCandy == 1 else self.cupPrice2
            side = 'left' if self.selectedCandy == 1 else 'right'

            if c.volume > MageHand.minVolume:
                self.machine.showSelectionMessage(f'{c.name} selected ({100*cupPrice[0]:.2f} / 100 mL) \n Move {side} to select other candy \n There is {c.volume:.2f} mL of this candy left \n Do a Peace Gesture to confirm', "Candy" + str(self.selectedCandy), ['Peace'])
            else:
                self.machine.showGestureMessage(f"There is no {c.name} left,\n please choose another candy", "Warning", [])
            return "selection"

        def peace_callback(Xpositions, **kargs):
            if self.selectedCandy == None:
                mean = sum(Xpositions) / len(Xpositions)
                self.selectedCandy = 1 if mean < 0.5 else 2

            c = self.candy1 if self.selectedCandy == 1 else self.candy2
            self.machine.showGestureMessage(f"Peace detected \n hold for 4 seconds to \n buy {c.name}", "Confirm", ["Candy" + str(self.selectedCandy), "Peace"])
            return "selection"
        def thumbsDown_callback(**kargs):
            self.machine.showGestureMessage("Thumbs Down detected \n hold for 4 seconds to \n cancel the order", "Confirm", ["ThumbsDown"])
            return "selection"
        def none_callback(**kargs):
            self.machine.showGestureMessage("Lost track of hand \n Select a candy with a Stop gesture \n to continue", "Alert", ["Stop"])
            return "selection"

        peace_confirmationCallback = lambda **kargs: "pouring"
        def thumbsDown_None_confirmationCallback(**kargs):
            self.machine.showGestureMessage("Rejecting candies and returning \n to introduction", "Alert", [])
            self.rejectCandies("Lost track of user")
            return "introduction"

        return self.gestureRecognizer.runState("selection",
                ["Undefined", "None", "Peace", "ThumbsDown"]
                , { "Undefined": undefined_callback,
                    "None": none_callback,
                    "Peace": peace_callback,
                    "ThumbsDown": thumbsDown_callback
                },
                ["Peace", "ThumbsDown", "None"] ,
                {
                    "Peace": peace_confirmationCallback,
                    "ThumbsDown": thumbsDown_None_confirmationCallback,
                    "None": thumbsDown_None_confirmationCallback
                },
                {
                    "None": 30
                })

    """
        Function to initiate the pouring phase
    """
    def pouringPhaseFunction(self):
        self.stateFile.write_text("pouring")
        self.machine.showGestureMessage("Show a Fist to pour \n the candy into cup \n Show a Stop to stop", "Info", ["Fist", "Stop"])

        def thumbsDown_callback(**kargs):
            self.machine.stopPouringCandy(self.selectedCandy)
            self.machine.showGestureMessage("Thumbs Down detected \n hold it for 4 seconds to \n cancel the order", "Confirm", ["ThumbsDown"])
            return "pouring"

        def fist_callback(delta_ms, **kargs):
            cup = self.cupVolume1 if self.selectedCandy == 1 else self.cupVolume2
            cupPrice = self.cupPrice1 if self.selectedCandy == 1 else self.cupPrice2
            c = self.candy1 if self.selectedCandy == 1 else self.candy2

            if cup[0] > self.maxCupVolume:
                self.machine.stopPouringCandy(self.selectedCandy)
                self.machine.showGestureMessage("Stopped pouring candy \n The cup is full \n Show a Stop gesture to continue", "Warning", ["Stop"])
                return "pouring"

            if c.volume < MageHand.minVolume:
                self.machine.stopPouringCandy(self.selectedCandy)
                self.machine.showGestureMessage("Stopped pouring candy \n Storage is below critical volume. \n Show a Stop gesture to continue", "Warning", ["Stop"])
                return "pouring"

            self.machine.showBuyingMessage(f"Cup Capacity: {cup[0]:.2f} of {self.maxCupVolume:.2f} mL\n Available: {c.volume:.2f} mL\n Cup price: R$ {cupPrice[0]:.2f} \n Show a Stop gesture to stop", ["Candy" + str(self.selectedCandy), "Stop"])
            self.machine.pourCandy(self.selectedCandy)
            cup[0] += round(MageHand.volumePerSecond * delta_ms / 1000, 2)
            c.volume -= round(MageHand.volumePerSecond * delta_ms / 1000, 2)
            cupPrice[0] = round(c.price * cup[0] / 8, 2)
            return "pouring"


        def undefined_callback(**kargs):
            cup = self.cupVolume1 if self.selectedCandy == 1 else self.cupVolume2
            cupPrice = self.cupPrice1 if self.selectedCandy == 1 else self.cupPrice2
            self.machine.showGestureMessage(f"Cup with {cup[0]:.2f} of {self.maxCupVolume:.2f} mL (R$ {cupPrice[0]:.2f})\n Show a Fist to pour more \n Show a Stop to stop", "Info", ["Fist", "Stop"])
            self.machine.stopPouringCandy(self.selectedCandy)
            return "pouring"

        def stop_callback(**kargs):
            self.machine.stopPouringCandy(self.selectedCandy)
            self.machine.showGestureMessage(f"Stop detected\nhold it for 4 seconds\n Current total price: R$ {self.cupPrice1[0] + self.cupPrice2[0]:.2f}", "Confirm", ["Stop"])
            self.storage1.write_text("{:.2f}".format(self.candy1.volume))
            self.storage2.write_text("{:.2f}".format(self.candy2.volume))
            self.cupFile1.write_text("{:.2f}".format(self.cupVolume1[0]))
            self.cupFile2.write_text("{:.2f}".format(self.cupVolume2[0]))
            return "pouring"
        def none_callback(**kargs):
            cup = self.cupVolume1 if self.selectedCandy == 1 else self.cupVolume2
            cupPrice = self.cupPrice1 if self.selectedCandy == 1 else self.cupPrice2
            self.machine.showGestureMessage(f"Lost track of hand \n Show your hand to continue \n Cup with {cup[0]:.2f} of {self.maxCupVolume:.2f} mL (R$ {cupPrice[0]:.2f})", "Alert", ["Peace"])
            return "pouring"

        def thumbsDown_confirmationCallback(**kargs):
            self.machine.showGestureMessage("Rejecting candies and returning \n to introduction", "Alert", [])
            self.rejectCandies("Order was cancelled in Pouring phase")
            return "introduction"
        stop_confirmationCallback = lambda **kargs: "decision"
        def none_confirmationCallback(**kargs):
            self.machine.showGestureMessage("Rejecting candies and returning \n to introduction", "Alert", [])
            self.rejectCandies("Lost track of customer in Pouring phase")
            return "introduction"


        return self.gestureRecognizer.runState("pouring",
                ["ThumbsDown", "Fist", "Undefined", "Stop", "None"],
                { "ThumbsDown": thumbsDown_callback,
                  "Fist": fist_callback,
                  "Undefined": undefined_callback,
                  "Stop": stop_callback,
                  "None": none_callback
                 },
                ["ThumbsDown", "Stop", "None"],
                { "ThumbsDown": thumbsDown_confirmationCallback,
                  "Stop": stop_confirmationCallback,
                  "None": none_confirmationCallback
                },
                {
                    "None": 30
                })


    """
        Function to initiate the decision phase
    """
    def decisionPhaseFunction(self):
        self.stateFile.write_text("decision")
        self.machine.showGestureMessage(f"Current total price: R$ {self.cupPrice1[0] + self.cupPrice2[0]:.2f} \n Thumbs Down will cancel the order \n Thumbs Up will go to payment \n Peace will return to buying candy", "Info", ["ThumbsUp", "ThumbsDown", "Peace"])

        def undefined_callback(**kargs):
            self.machine.showGestureMessage(f"Current total price: R$ {self.cupPrice1[0] + self.cupPrice2[0]:.2f} \n Thumbs Down will cancel the order \n Thumbs Up will go to payment \n Peace will return to buying candy", "Info", ["ThumbsUp", "ThumbsDown", "Peace"])
            return "decision"

        def general_callback(gesture):
            def callback(**kargs):
                self.machine.showGestureMessage(f"Hold the {MageHand.name_conversion[gesture]} gesture\n for 4 seconds to {MageHand.action_conversion[gesture]} \n Current total price: R$ {self.cupPrice1[0] + self.cupPrice2[0]:.2f}", "Confirm", [gesture])
                return "decision"
            return callback

        def none_callback(**kargs):
            self.machine.showGestureMessage(f"Lost track of hand \n Show your hand to continue \n Current total price: R$ {self.cupPrice1[0] + self.cupPrice2[0]:.2f}", "Alert", ["Stop"])
            return "decision"

        def thumbsDown_confirmationCallback(**kargs):
            self.machine.showGestureMessage("Rejecting candies and returning \n to introduction", "Alert", [])
            self.rejectCandies("Order was cancelled in decision phase")
            return "introduction"

        thumbsUp_confirmationCallback = lambda **kargs: "payment"
        peace_confirmationCallback = lambda **kargs: "selection"

        def none_confirmationCallback(**kargs):
            self.machine.showGestureMessage("Rejecting candies and returning \n to introduction", "Alert", [])
            self.rejectCandies("Lost track of customer in decision phase")
            return "introduction"

        return self.gestureRecognizer.runState("decision",
                                               ["ThumbsDown", "ThumbsUp", "Peace", "None", "Undefined"],
                                               {"ThumbsDown": general_callback("ThumbsDown"),
                                                "ThumbsUp": general_callback("ThumbsUp"),
                                                "Peace": general_callback("Peace"),
                                                "None": none_callback,
                                                "Undefined": undefined_callback
                                               },
                                               ["ThumbsDown", "ThumbsUp", "Peace", "None"],
                                               {"ThumbsDown": thumbsDown_confirmationCallback,
                                                "ThumbsUp":thumbsUp_confirmationCallback,
                                                "Peace": peace_confirmationCallback,
                                                "None": none_confirmationCallback
                                               },
                                                {
                                                    "None": 30
                                                }
                                               )
    """
        Function to initiate the payment phase
    """
    def paymentPhaseFunction(self):
        self.stateFile.write_text("payment")

        while not is_connected():
            self.machine.showGestureMessage("No Internet Connection \n Please Wait", "Alert", [])
            sleep(1)

        self.machine.showGestureMessage("Generating payment, please wait", "Confirm", ["Peace"])
        successEvent = threading.Event()
        failureEvent = threading.Event()
        amount = (self.cupPrice1[0]) + (self.cupPrice2[0])
        if "--accept" in sys.argv:
            self.machine.showGestureMessage("Payment was accepted \n Please collect your candy", "Info", [])
            self.acceptCandies("Payment Successful")
            sleep(2)
            return "introduction"
        elif "--reject" in sys.argv:
            self.machine.showGestureMessage("Order was canceled", "Alert", [])
            self.rejectCandies("Order was cancelled")
            sleep(2)
            return "introduction"

        if "--test" not in sys.argv:
            import pygame
            import base64
            import io
            qrcode_b64 = self.paymentManager.createPayment(amount=round(amount, 2), description="candy bought with mage hand")
            if not qrcode_b64:
                self.machine.showGestureMessage("Error creating payment \n Order cancelled", "Alert", ["ThumbsDown"])
                self.rejectCandies("Order was cancelled")
                sleep(5)
                return "introduction"
            qrcode = base64.b64decode(qrcode_b64)
            mem_file = io.BytesIO(qrcode)
            qrcode_img = pygame.image.load(mem_file)
            qrcode_img = pygame.transform.scale(qrcode_img, (240, 240))


        def thread1():
            while True:
                status = self.paymentManager.checkPayment()
                # print(f"status checked: {status}")
                if status == "cancelled":
                    failureEvent.set()
                    break
                elif status == "approved":
                    successEvent.set()
                    break
                sleep(10)

        def thread2():
            def thumbsDown_callback(**kargs):
                self.machine.showGestureMessage("Hold Thumbs Down \n for 4 seconds to cancel", "Confirm", ["ThumbsDown"])
                return "introduction" if successEvent.is_set() or failureEvent.is_set() else "payment"

            def thumbsDown_confirmationCallback(**kargs):
                self.machine.showGestureMessage("Canceling order", "Alert", [])
                self.paymentManager.cancelPayment()
                return "introduction"

            def normal_callback(**kargs):
                self.machine.showGestureMessage(f"QRcode for payment of R$ {round(amount, 2):.2f}", "Confirm", ["ThumbsUp"], pos=(80, 24))
                self.machine.showImage(qrcode_img, make_surface=False, clear=False, pos=(120, 70))
                return "introduction" if successEvent.is_set() or failureEvent.is_set() else "payment"
                

            self.gestureRecognizer.runState("payment",["ThumbsDown", "Undefined", "None"], { "ThumbsDown": thumbsDown_callback, "None": normal_callback, "Undefined": normal_callback}, ["ThumbsDown"], {"ThumbsDown": thumbsDown_confirmationCallback})

        paymentThread = threading.Thread(target=thread1)
        expirationTimer = threading.Timer(300, self.paymentManager.cancelPayment)
        gestureThread = threading.Thread(target=thread2)

        paymentThread.start()
        gestureThread.start()
        expirationTimer.start()

        paymentThread.join()
        gestureThread.join()

        if successEvent.is_set():
            self.machine.showGestureMessage("Payment was accepted \n please collect your candy", "Info", [])
            self.acceptCandies("Payment Successful")
        else:
            self.machine.showGestureMessage("Order was cancelled", "Alert", [])
            self.rejectCandies("Order was cancelled")


        return "introduction"

    def syncFirebase(self, ignore=False):
        if (not ignore) and (not self.sync.is_set()):
            return
        self.sync.clear()
        self.machine.showGestureMessage("Syncing with remote database \n Please wait", "Info", [])
        self.getFirebaseCandyInformation()
        sleep(1)
        if not self.sync.is_set():
            return
        self.machine.showGestureMessage("Inconsistency detected \n Retrieving updated information \n from database", "Alert", [])
        sleep(2)

    """
        Function to set up firebase listener
    """
    def firebaseCallbackFunction(self):
        response = requests.get(MageHand.firebase_url + self.user + "/candyInformation.json", stream=True, headers={"Accept": "text/event-stream"})
        client = sseclient.SSEClient(response)
        # print("Firebase notifications are now enabled")
        for event in client.events():
            # print(f"Received event {event}")
            # print(event.event)
            data = json.loads(event.data)
            if event.event == 'put' or event.event == "patch":
                self.sync.set()
            # if event.event == 'put':
            #     print(f"put: {data}")
            # elif event.event == "patch":
            #     print(f"patch: {data}")
            requests.post(MageHand.functions_url + "/machine_is_online", params={"uid": self.user})



    def getFirebasePaymentKeys(self):
        response = requests.get(MageHand.firebase_url + self.user + "/PaymentKeys.json")
        if response.status_code in [200, 201]:
            json_resp = response.json()
            self.paymentManager.setPaymentKeys(json_resp["accessToken"])

    def getFirebaseCandyInformation(self):
        response = requests.get(MageHand.candy_1_storage_url)
        if response.status_code in [200, 201]:
           with open('images/candy1.png', 'wb') as candy1:
               candy1.write(response.content)
        response = requests.get(MageHand.candy_2_storage_url)
        if response.status_code in [200, 201]:
           with open('images/candy2.png', 'wb') as candy2:
               candy2.write(response.content)
        
        response = requests.get(MageHand.firebase_url + self.user + "/candyInformation.json")
        if response.status_code in [200, 201]:
            json_resp = response.json()
            # print(json_resp)
            c1 = json_resp["Candy1"]
            c2 = json_resp["Candy2"]
            c1["Image"] = 'images/candy1.png'
            c2["Image"] = 'images/candy2.png'
            newVolume1 = float(c1["Replenish"]) + self.candy1.volume
            newVolume2 = float(c2["Replenish"]) + self.candy2.volume
            self.candy1 = Candy(c1["Name"], float(c1["Price"]), newVolume1, c1["Image"])
            self.candy2 = Candy(c2["Name"], float(c2["Price"]), newVolume2, c2["Image"])
            (self.dataDir / "candyInformation.json").write_text(json.dumps({"Candy1": c1, "Candy2": c2}))
            response2 = requests.patch(MageHand.firebase_url + self.user + "/candyInformation.json", data=json.dumps({ "Candy1/Volume": self.candy1.volume, "Candy2/Volume": self.candy2.volume, "Candy1/Replenish": 0, "Candy2/Replenish": 0 }))

if __name__ == '__main__':
    mage = MageHand()
    try:
        p = mage.bootPhaseFunction()
        while True:
            p = mage.phases[p]()
    except KeyboardInterrupt:
        print("Machine is Turning Off")
        try:
            requests.post(MageHand.functions_url + "/machine_is_offline", params={"uid": mage.user}, timeout=0.5)
        except:
            pass