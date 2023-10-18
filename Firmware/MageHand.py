from PaymentManager import PaymentManager
from Machine import Machine
from GestureRecognizer import GestureRecognizer
from pathlib import Path
import json


class MageHand:
    def __init__(self) -> None:
        config = (Path.home() / ".config/MageHand/MageHAndParameters.json").read_text()
        params = json.loads(config)
        self.machine = Machine(params["displayParameters"], params["servoParameters"], params["motorParameters"])
        self.gestureRecognizer = GestureRecognizer()
        self.paymentManager = PaymentManager()
        self.tempDir = Path("/var/tmp/MageHand")
        self.tempDir.mkdir(exist_ok=True)
        self.stateFile = self.tempDir / "current_state.txt"

    def bootPhaseFunction(self):
        lastPhase = self.stateFile.read_text()
        if lastPhase == "payment":
            self.machine.acceptCandies()
        else:
            self.machine.rejectCandies()

        self.introductionPhaseFunction()


    def introductionPhaseFunction(self):
        self.stateFile.write_text("introduction")

    def confirmationPhaseFunction(self):
        self.stateFile.write_text("confirmation")

    def selectionPhaseFunction(self):
        self.stateFile.write_text("selection")

    def pouringPhaseFunction(self):
        self.stateFile.write_text("pouring")
        pass
    def decisionPhaseFunction(self):
        self.stateFile.write_text("decision")
        pass
    def paymentPhaseFunction(self):
        self.stateFile.write_text("payment")
        pass
    def firebaseCallbackFunction(self):
        pass
