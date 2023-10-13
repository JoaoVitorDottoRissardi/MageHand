import cv2
import operator
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
        self.callbacks = {}

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


        # Create a hand landmarker instance with the video mode:
        while True:
            ret, frame = cap.read()
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            frame1 = cv2.resize(frame, (640, 480))
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
            hand_landmarker_result = self.landmarker.detect_for_video(mp_image, int(timestamp))

            landmarks = []

            for xablau in hand_landmarker_result.hand_landmarks:
                print(xablau)
                for landmark in xablau:
                    l = []
                    l.append(landmark.x)
                    l.append(landmark.y)
                    l.append(landmark.z)
                    landmarks.append(l)

            if landmarks != []:
                score_label = predict_by_geometry([landmarks], self.known_finger_poses, 0.45)
                print(score_label)

    def setCallback(self, gesture, function, confirm_time=0, frame_tolerance=0):
        if gesture not in self.known_finger_poses:
            return False
        self.callbacks[(gesture, confirm_time, frame_tolerance)] = function
        return True


    def resetCallbacks(self):
        self.callbacks = {}
