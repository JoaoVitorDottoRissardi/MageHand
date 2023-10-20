from PaymentManager import PaymentManager
from Machine import Machine
from GestureRecognizer import GestureRecognizer
from pathlib import Path # needs python 3.4
import json
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
    def __init__(self):
        config = (Path.home() / ".config/MageHand/MageHandParameters.json").read_text()
        params = json.loads(config)

        self.machine = Machine(params["displayParameters"], params["servoParameters"], params["motorParameters"])
        self.gestureRecognizer = GestureRecognizer()
        self.paymentManager = PaymentManager()

        self.dataDir = Path("/var/lib/MageHand")
        self.dataDir.mkdir(exist_ok=True)

        candyFile = (self.dataDir / "candyInformation.json").read_text()
        candyData = json.loads(candyFile)
        c1 = candyData["candy1"]
        c2 = candyData["candy2"]
        self.candy1 = Candy(c1["name"], c1["price"], c1["volume"], c1["image"])
        self.candy2 = Candy(c2["name"], c2["price"], c2["volume"], c2["image"])

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
        lastPhase = self.stateFile.read_text()
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
        self.machine.showGestureMessage('Make a Stop sign to proceed', 'Info', ['Peace', 'Stop', 'ThumbsUp'])
        return self.gestureRecognizer.runState("introduction", ["Stop"], {}
                                        , ["Stop"],{"Stop": lambda *args: "confirmation"})


    """
        Function to initiate the confirmation phase
    """
    def confirmationPhaseFunction(self):
        self.stateFile.write_text("confirmation")
        self.machine.showGestureMessage('Customer Detected \n Do a Thumbs Up to Buy Candy', 'Info', ["ThumbsUp"])
        return self.gestureRecognizer.runState("confirmation", ["ThumbsUp", "None"], {"ThumbsUp": lambda *args: "selection"}
                                        , ["None"],{"None": lambda *args: "introduction"})

    """
        TODO: Function to initiate the selection phase
    """
    def selectionPhaseFunction(self):
        self.stateFile.write_text("selection")

    """
        TODO: Function to initiate the pouring phase
    """
    def pouringPhaseFunction(self):
        self.stateFile.write_text("pouring")
        pass
    """
        TODO: Function to initiate the decision phase
    """
    def decisionPhaseFunction(self):
        self.stateFile.write_text("decision")
        pass
    """
        TODO: Function to initiate the payment phase
    """
    def paymentPhaseFunction(self):
        self.stateFile.write_text("payment")
        pass
    """
        TODO: Function to set up firebase listener
    """
    def firebaseCallbackFunction(self):
        pass


if __name__ == '__main__':
    mage = MageHand()
    p = mage.bootPhaseFunction()
    while True:
        p = mage.phases[p]()
