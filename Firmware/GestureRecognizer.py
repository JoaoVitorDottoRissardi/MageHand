import cv2
import operator
import time
import mediapipe as mp
from mediapipe.tasks import BaseOptions
from mediapipe.tasks.vision import HandLandmarker, HandLandmarkerOptions, VisionRunningMode
from pose.utils.FingerPoseEstimate import FingerPoseEstimate
from pose.DeterminePositions import create_known_finger_poses, determine_position, get_position_name_with_pose_id
"""
Class for handling gesture recognition and callback assignment

Attributes
----------

"""
class GestureRecognizer:

    def __init__(self):
        self.known_finger_poses = create_known_finger_poses()
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
            running_mode=VisionRunningMode.VIDEO)
        self.landmarker = HandLandmarker.create_from_options(options)
        self.confirmationFlag = False
        self.confirmationGesture = "None"
        self.callbacks = { k.position_name:(False, lambda *args, **kwargs: None) for k in self.known_finger_poses }
        self.callbacks = { k.position_name:(0, lambda *args, **kwargs: None) for k in self.known_finger_poses }

    def run(self):
        cap = cv2.VideoCapture(0)

        def predict_by_geometry(keypoint_coord3d_v, known_finger_poses, threshold):
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

            print(obtained_positions)
            return score_label


        countdown = 3
        timer = time.perf_counter_ns()
        current_gesture = "None"
        gesture_count = { k.position_name:0 for k in self.known_finger_poses }
        # Create a hand landmarker instance with the video mode:
        while True:
            gesture = "None"
            ret, frame = cap.read()
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            frame1 = cv2.resize(frame, (640, 480))
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
            hand_landmarker_result = self.landmarker.detect_for_video(mp_image, int(timestamp))

            landmarks = []

            for result in hand_landmarker_result.hand_landmarks:
                for landmark in result:
                    l = []
                    l.append(landmark.x)
                    l.append(landmark.y)
                    l.append(landmark.z)
                    landmarks.append(l)

            if landmarks != []:
                score_label = predict_by_geometry([landmarks], self.known_finger_poses, 0.45)
                print(score_label)
                gesture = score_label

            gesture_count[gesture] =+ 1
            if gesture_count[gesture] > 10:
                if self.confirmationFlag:
                    if gesture != current_gesture:
                        self.confirmationFlag = False
                        timer = 0
                    else:
                        continue
                current_gesture = gesture
                gesture_count = { k.position_name:0 for k in self.known_finger_poses }
                self.callbacks[gesture][1]()
                if self.callbacks[gesture][0]:
                    self.confirmationFlag = True
                    timer = time.perf_counter_ns()


    def setCallback(self, gesture, function=lambda *args, **kwargs: None, min_time=0, confirmationFunction=lambda *args, **kwargs: None):
        if gesture not in [ f.position_name for f in self.known_finger_poses ]:
            return False
        self.callbacks[gesture] = (min_time > 0, function)
        self.confirmationCallbacks[gesture] = (min_time, confirmationFunction)
        return True


    def resetCallbacks(self):
        self.callbacks = {}
