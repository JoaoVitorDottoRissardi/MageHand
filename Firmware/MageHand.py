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
import sseclient # sseclient-py
from dataclasses import dataclass # needs python 3.7

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

class MageHand:
    firebase_url = "https://mage-hand-demo-default-rtdb.firebaseio.com/"
    minVolume = 10
    maxCupVolume = 100
    volumePerTurn = 10
    def __init__(self):
        config = (Path.home() / ".config/MageHand/MageHandParameters.json").read_text()
        params = json.loads(config)

        self.machine = Machine(params["displayParameters"], params["servoParameters"], params["motorParameters"])
        self.gestureRecognizer = GestureRecognizer()
        self.paymentManager = PaymentManager()

        self.firebaseThread = threading.Thread(target=self.firebaseCallbackFunction)

        self.dataDir = Path("/var/lib/MageHand")
        self.dataDir.mkdir(exist_ok=True)

        if (self.dataDir / "candyInformation.json").exists():
            candyFile = (self.dataDir / "candyInformation.json").read_text()
            candyData = json.loads(candyFile)
            c1 = candyData["Candy1"]
            c2 = candyData["Candy2"]
            self.candy1 = Candy(c1["Name"], c1["Price"], c1["Volume"], c1["Image"])
            self.candy2 = Candy(c2["Name"], c2["Price"], c2["Volume"], c2["Image"])
        else:
            self.getFirebaseCandyInformation()

        self.selectedCandy = None
        self.stateFile = self.dataDir / "current_state.txt"

        self.phases = {
            "boot": self.bootPhaseFunction,
            "introduction": self.introductionPhaseFunction,
            "confirmation": self.confirmationPhaseFunction,
            "selection": self.selectionPhaseFunction,
            "pouring": self.pouringPhaseFunction,
            "decision": self.decisionPhaseFunction,
            "payment": self.paymentPhaseFunction
        }

    """
        Function to initiate the boot phase
    """
    def bootPhaseFunction(self):
        lastPhase = self.stateFile.read_text() if self.stateFile.exists() else ""

        self.getFirebaseCandyInformation()
        self.firebaseThread.start()

        if lastPhase == "payment":
            self.machine.acceptCandies()
        else:
            self.machine.rejectCandies()

        return "introduction"


    """
        Function to initiate the introduction phase
    """
    def introductionPhaseFunction(self):
        self.stateFile.write_text("introduction")
        self.cupVolume1 = [0]
        self.cupVolume2 = [0]

        if not self.paymentManager.hasPaymentKeys():
            self.machine.showGestureMessage('There are no payment keys configured \n Cannot proceed', 'Alert', [])
            self.getFirebasePaymentKeys()

        self.machine.showGestureMessage('Make a Stop sign to proceed', 'Info', ['Stop'])
        return self.gestureRecognizer.runState("introduction", ["Stop"], {}
                                        , ["Stop"],{"Stop": lambda **kargs: "confirmation"})


    """
        Function to initiate the confirmation phase
    """
    def confirmationPhaseFunction(self):
        self.stateFile.write_text("confirmation")
        self.machine.showGestureMessage('Customer Detected \n Do a Thumbs Up to Buy Candy', 'Info', ["ThumbsUp"])
        return self.gestureRecognizer.runState("confirmation", ["ThumbsUp", "None"], {"ThumbsUp": lambda **kargs: "selection"}
                                        , ["None"],{"None": lambda **kargs: "introduction"})

    """
        Function to initiate the selection phase
    """
    def selectionPhaseFunction(self):
        self.stateFile.write_text("selection")
        self.machine.showGestureMessage('Select a Candy Type', 'Info', ["ThumbsUp"])

        def undefined_callback(Xpositions):
            mean = sum(Xpositions) / len(Xpositions)

            self.selectedCandy = 1 if mean < 320 else 2
            c = self.candy1 if self.selectedCandy == 1 else self.candy2

            if c.volume > MageHand.minVolume:
                self.machine.showSelectionMessage(f'{c.name} selected', "Candy" + str(self.selectedCandy))
            else:
                self.machine.showGestureMessage(f"There is no {c.name} left, please choose another type", "Alert", [])
            return "selection"

        def thumbsUp_callback(**kargs):
            self.machine.showGestureMessage("Thumbs Up detected, hold for 4 seconds", "Info", ["ThumbsUp"])
            return "selection"
        def thumbsDown_callback(**kargs):
            self.machine.showGestureMessage("Thumbs Down detected \n hold for 4 seconds", "Info", ["ThumbsUp"])
            return "selection"
        def none_callback(**kargs):
            self.machine.showGestureMessage("Lost track of hand", "Alert", [])
            return "selection"

        thumbsUp_confirmationCallback = lambda **kargs: "pouring"
        def thumbsDown_None_confirmationCallback(**kargs):
            self.machine.rejectCandies()
            return "introduction"

        return self.gestureRecognizer.runState("selection",
                ["Undefined", "None", "ThumbsUp", "ThumbsDown"]
                , { "Undefined": undefined_callback,
                    "None": none_callback,
                    "ThumbsUp": thumbsUp_callback,
                    "ThumbsDown": thumbsDown_callback
                },
                ["ThumbsUp", "ThumbsDown", "None"] ,
                {
                    "ThumbsUp": thumbsUp_confirmationCallback,
                    "ThumbsDown": thumbsDown_None_confirmationCallback,
                    "None": thumbsDown_None_confirmationCallback
                })

    """
        Function to initiate the pouring phase
    """
    def pouringPhaseFunction(self):
        self.stateFile.write_text("pouring")
        self.machine.showGestureMessage("Show a Fist to pour \n the candy into cup", "Info", ["Fist"])

        def thumbsDown_callback(**kargs):
            self.machine.stopPouringCandy(self.selectedCandy)
            self.machine.showGestureMessage("Thumbs Down detected \n hold it for 4 seconds", "Confirm", ["ThumbsDown"])
            return "pouring"
        def fist_callback(**kargs):

            cup = self.cupVolume1 if self.selectedCandy == 1 else self.cupVolume2
            c = self.candy1 if self.selectedCandy == 1 else self.candy2

            if cup[0] > self.maxCupVolume:
                self.machine.showGestureMessage("The cup will overflow", "Alert", [])
                self.machine.stopPouringCandy(self.selectedCandy)
                return "pouring"

            if c.volume < MageHand.minVolume:
                self.machine.showGestureMessage("Storage is below critical volume. \n Please show a Stop gesture", "Info", ["Stop"])
                self.machine.stopPouringCandy(self.selectedCandy)
                return "pouring"

            self.machine.showBuyingMessage(f"Cup Capacity: {cup[0]} of {self.maxCupVolume} \n Available: {c.volume}\n Total price: {cup[0]*c.price}", ["Candy" + str(self.selectedCandy)])
            self.machine.pourCandy(self.selectedCandy)
            cup[0] += MageHand.volumePerTurn
            c.volume -= MageHand.volumePerTurn
            return "pouring"


        def undefined_callback(**kargs):
            self.machine.stopPouringCandy(self.selectedCandy)
            return "pouring"

        def stop_callback(**kargs):
            self.machine.stopPouringCandy(self.selectedCandy)
            self.machine.showGestureMessage("Stop detected, hold it for 4 seconds", "Confirm", ["Stop"])
            return "pouring"
        def none_callback(**kargs):
            self.machine.showGestureMessage("lost track of hand", "Alert", [])
            return "pouring"

        def thumbsDown_confirmationCallback(**kargs):
            self.machine.rejectCandies()
            return "introduction"
        stop_confirmationCallback = lambda **kargs: "decision"
        def none_confirmationCallback(**kargs):
            self.machine.rejectCandies()
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
                })


    """
        Function to initiate the decision phase
    """
    def decisionPhaseFunction(self):
        self.stateFile.write_text("decision")
        self.machine.showGestureMessage("Thumbs Down will reject the purchase \n Thumbs Up will go to payment \n Peace will return to buying candy", "Info", ["ThumbsUp", "ThumbsDown", "Peace"])

        def general_callback(**kargs):
            self.machine.showGestureMessage("hold the gesture for 4 seconds", "Confirm", [])
            return "decision"

        def none_callback(**kargs):
            self.machine.showGestureMessage("lost track of hand", "Alert", [])
            return "decision"

        def thumbsDown_confirmationCallback(**kargs):
            self.machine.rejectCandies()
            return "introduction"

        thumbsUp_confirmationCallback = lambda **kargs: "payment"
        peace_confirmationCallback = lambda **kargs: "selection"

        def none_confirmationCallback(**kargs):
            self.machine.rejectCandies()
            return "introduction"

        return self.gestureRecognizer.runState("decision",
                                               ["ThumbsDown", "ThumbsUp", "Peace", "None"],
                                               {"ThumbsDown": general_callback,
                                                "ThumbsUp": general_callback,
                                                "Peace": general_callback,
                                                "None": none_callback
                                               },
                                               ["ThumbsDown", "ThumbsUp", "Peace", "None"],
                                               {"ThumbsDown": thumbsDown_confirmationCallback,
                                                "ThumbsUp":thumbsUp_confirmationCallback,
                                                "Peace": peace_confirmationCallback,
                                                "None": none_confirmationCallback
                                               }
                                               )
    """
        Function to initiate the payment phase
    """
    def paymentPhaseFunction(self):
        self.stateFile.write_text("payment")

        successEvent = threading.Event()
        failureEvent = threading.Event()
        gestureEvent = threading.Event()
        amount = (self.candy1.price * self.cupVolume1[0]) + (self.candy2.price * self.cupVolume2[0])
        if "--test" not in sys.argv:
            self.paymentManager.createPayment(amount=amount, description="candy bought with mage hand")

        def thread1():
            while True:
                if gestureEvent.is_set():
                    break
                status = self.paymentManager.checkPayment()
                if status == "cancelled":
                    failureEvent.set()
                    break
                elif status == "approved":
                    successEvent.set()
                    break

        def thread2():
            def thumbsDown_callback(**kargs):
                self.machine.showGestureMessage("Hold Thumbs Down for 4 seconds to cancel", "Confirm", ["ThumbsDown"])
                return "introduction" if successEvent.is_set() or failureEvent.is_set() else "payment"
            def thumbsDown_confirmationCallback(**kargs):
                gestureEvent.set()
                return "introduction"

            self.gestureRecognizer.runState("payment",["ThumbsDown"], { "ThumbsDown": thumbsDown_callback }, ["ThumbsDown"], {"ThumbsDown": thumbsDown_confirmationCallback})

        paymentThread = threading.Thread(target=thread1)
        gestureThread = threading.Thread(target=thread2)

        paymentThread.start()
        gestureThread.start()

        paymentThread.join()
        gestureThread.join()

        if successEvent.is_set():
            self.machine.showGestureMessage("Payment was accepted \n please collect your candy", "Info", [])
            self.machine.acceptCandies()
        else:
            self.machine.showGestureMessage("Order was canceled", "Alert", [])
            self.machine.rejectCandies()


        return "introduction"

    """
        Function to set up firebase listener
    """
    def firebaseCallbackFunction(self):
        response = requests.get(MageHand.firebase_url, stream=True, headers={"Accept": "text/event-stream"})
        client = sseclient.SSEClient(response)
        print("Firebase notifications are now enabled")
        for event in client.events():
            data = json.loads(event.data)
            match event.event:
                case "put":
                    print("put: " + data)
                case "patch":
                    print("patch: " + data)



    def getFirebasePaymentKeys(self):
        response = requests.get(MageHand.firebase_url + "/PaymentKeys.json")
        if response.status_code in [200, 201]:
            json_resp = response.json()
            self.paymentManager.setPaymentKeys(json_resp["publicKey"], json_resp["accessToken"], json_resp["payerData"])

    def getFirebaseCandyInformation(self):
        response = requests.get(MageHand.firebase_url + "/candyInformation.json")
        if response.status_code in [200, 201]:
            json_resp = response.json()
            print(json_resp)
            c1 = json_resp["Candy1"]
            c2 = json_resp["Candy2"]
            self.candy1 = Candy(c1["Name"], c1["Price"], c1["Volume"], c1["Image"])
            self.candy2 = Candy(c2["Name"], c2["Price"], c2["Volume"], c2["Image"])
            (self.dataDir / "candyInformation.json").write_text(response.text)

if __name__ == '__main__':
    mage = MageHand()
    p = mage.bootPhaseFunction()
    while True:
        p = mage.phases[p]()
