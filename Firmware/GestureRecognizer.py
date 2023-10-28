import mediapipe as mp
import numpy as np
import cv2
from pose.utils.FingerPoseEstimate import FingerPoseEstimate
from pose.DeterminePositions import create_known_finger_poses, determine_position, get_position_name_with_pose_id
import operator
import time

"""
Class that provides the means to run gesture detection for gestures of interest,
running the provided callbacks depending of the detections, stopping depending on
the return values of the callbacks executed

Attributes
----------

cap: cv2.VideoCapture
    VideoCapture of opencv

known_finger_poses: list[FingerDataFormation]
    the known gestures, as defined inside "DeterminePositions.py"

landmarker: HandLandmarker
    the object from mediapipe that detects landmarks in images

Construcutor params
-------------------

"""

class GestureRecognizer:

    def __init__(self):

        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise Exception('a')
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        self.known_finger_poses = create_known_finger_poses()

        # Create a hand landmarker instance with the video mode:
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
            running_mode=VisionRunningMode.VIDEO)

        self.landmarker = HandLandmarker.create_from_options(options)


    """
        Close landmarker in destructor

    """

    def __del__(self):
        self.landmarker.close()
        pass

    """
        Function that returns detected gesture based on the landmarks sent

        Parameters
        ----------

        keypoint_coord3d_v: list[list[list[float]]]
            each landmark is a list of 3 float elements (x, y, z)
        
        known_finger_poses: list[FingerDataFormation]
            the known gestures, as defined inside "DeterminePositions.py"
        
        threshold: float
            if a gesture gets a score lower than the threshold, it is not considered

    """

    def predict_by_geometry(self, keypoint_coord3d_v, known_finger_poses, threshold):
        fingerPoseEstimate = FingerPoseEstimate(keypoint_coord3d_v)
        fingerPoseEstimate.calculate_positions_of_fingers(print_finger_info = True)
        obtained_positions = determine_position(fingerPoseEstimate.finger_curled, 
                                            fingerPoseEstimate.finger_position, known_finger_poses,
                                            threshold * 10)

        score_label = 'Undefined'
        if len(obtained_positions) > 0:
            max_pose_label = max(obtained_positions.items(), key=operator.itemgetter(1))[0]
            if obtained_positions[max_pose_label] >= threshold:
                score_label = max_pose_label
        
        # print(obtained_positions)
        return score_label

    """
        Function to run the gesture detection for gestures of interest, running
        the provided callbacks while the state remains the same

        Parameters
        ----------

        state: str
            current state. When some callback returns something different than that string,
            the detection will stop and the system will transition to this new returned state
        
        gestures_of_interest: list[str]
            a list with the 'position_name' field of the gestures we are looking for now
        
        gesture_started_callbacks: dict[str] -> function
            dictionary of the callbacks to be run when some gesture starts to be recognized,
            with the keys being the gestures of interest
        
        gestures_to_be_confirmed: list[str]
            a list with the 'position_name' field of the gestures we wait for confirmation
        
        gesture_confirmed_callbacks: dict[str] -> function
            dictionary of the callbacks to be run after the confirmation time passes with
            the gesture being done
    """

    def runState(
        self,
        state,
        gestures_of_interest,
        gesture_started_callbacks,
        gestures_to_be_confirmed,
        gesture_confirmed_callbacks
    ):
        def nop(**kargs):
            return state
        # fill dictionaries of callbacks if they aren't yet
        for g in gestures_of_interest:
            if g not in gesture_started_callbacks.keys():
                gesture_started_callbacks[g] = nop
        
        for g in gestures_to_be_confirmed:
            if g not in gesture_confirmed_callbacks.keys():
                gesture_confirmed_callbacks[g] = nop

        # variables to manage gesture recognizer
        in_confirmation = 'No'
        times_to_really_detect = 3
        last_gesture = 'Undefined'
        current_gesture_count = 0
        # detected_gestures = ['Undefined'] * times_to_really_detect
        # curr_idx = 0
        detected_gestures = []
        confirmation_time_delta = 4 # in seconds

        while True:
            ret, frame = self.cap.read()
            timestamp = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp = time.monotonic_ns()
            frame1 = cv2.resize(frame, (640, 480)) 
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
            hand_landmarker_result = self.landmarker.detect_for_video(mp_image, int(timestamp))
            
            # magic conversion to expected landmarks format
            landmarks = []
            Xpositions = []
            for xablau in hand_landmarker_result.hand_landmarks:
                # print(xablau)
                for landmark in xablau:
                    l = []
                    l.append(landmark.x)
                    l.append(landmark.y)
                    l.append(landmark.z)
                    landmarks.append(l)
                    Xpositions.append(landmark.x)
            
            score_label = 'Undefined'
            if landmarks != []:
                score_label = self.predict_by_geometry([landmarks], self.known_finger_poses, 0.45)
            else:
                score_label = "None"



            if in_confirmation == 'No':
                if score_label != last_gesture:
                    last_gesture = score_label
                    current_gesture_count = 0
                
                if score_label in gestures_of_interest:
                    current_gesture_count += 1

                if current_gesture_count >= times_to_really_detect:
                    # print(f"starting detection of '{score_label}'")
                    new_state = gesture_started_callbacks[score_label](Xpositions=Xpositions, frame=frame1)
                    if new_state != state:
                        return new_state

                    if score_label in gestures_to_be_confirmed:
                        in_confirmation = score_label
                        detected_gestures = []
                        confirmation_end = time.monotonic() + confirmation_time_delta
            else:
                detected_gestures.append(score_label)
                should_give_up = self.detect_abandoned_gesture(in_confirmation, detected_gestures)
                if should_give_up:
                    in_confirmation = 'No'
                    last_gesture = 'Undefined'
                    current_gesture_count = 0
                else:
                    curr_time = time.monotonic()
                    if curr_time >= confirmation_end:
                        # print(f"confirmed gesture '{in_confirmation}'")
                        new_state = gesture_confirmed_callbacks[in_confirmation]()
                        if new_state != state:
                            return new_state
                        in_confirmation = 'No'
                        last_gesture = 'Undefined'
                        current_gesture_count = 0


            # detected_gestures[curr_idx] = score_label
            # curr_idx = (curr_idx + 1) % times_to_really_detect


            # print(score_label)

    """
        Function to decide, based on the list of the detected gestures, if the gesture
        being confirmed was abandoned or not

        Parameters
        ----------

        in_confirmation: str
            the gesture being confirmed
        
        detected_gestures: list[str]
            a list with the gestures detected since the confirmation started
    """

    def detect_abandoned_gesture(self, in_confirmation, detected_gestures):
        # change this if needed
        max_frames_lost_in_row = 8
        max_percent_lost_in_total = 0.3

        lost = False
        lost_in_row = 0
        lost_in_total = 0
        for g in detected_gestures:
            if g != in_confirmation:
                lost_in_total += 1
                if not lost:
                    lost = True
                    lost_in_row = 0
                lost_in_row += 1
                if lost_in_row >= max_frames_lost_in_row:
                    return True
            else:
                lost = False
                lost_in_row = 0

        if lost_in_total / len(detected_gestures) >= max_percent_lost_in_total:
            return True
        
        # the confirmation can keep going
        return False

if __name__ == "__main__":
    import pygame
    g = GestureRecognizer()
    gestures = ["ThumbsUp", "ThumbsDown", "Peace", "Stop", "Fist", "None"]
    pathImages = {"ThumbsUp": "./images/thumbs_up.png", "ThumbsDown": "./images/thumbs_down.png","Peace": "./images/peace.png", "Stop": "./images/stop.png", "Fist": "./images/fist.png"}
    pygame.init()
    images = {k:pygame.image.load(v) for k,v in pathImages.items()}
    screen = pygame.display.set_mode((480,320), pygame.RESIZABLE)
    def showGesture(gesture):
        if gesture == "None":
            def c(frame, **kargs):
                frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)
                screen.blit(pygame.surfarray.make_surface(frame), (0,0))
                pygame.display.update()
                return "state"
            return c
        def show(**kargs):
            screen.fill([255,255,255])
            image = pygame.transform.scale_by(images[gesture], 0.2)
            screen.blit(image, (50, 50))
            pygame.display.update()
            return "state"
        return show
    g.runState("state", gestures, {k:showGesture(k) for k in gestures}, [], {})
