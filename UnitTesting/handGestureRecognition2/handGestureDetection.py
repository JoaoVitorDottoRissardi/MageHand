import mediapipe as mp
import cv2
from pose.utils.FingerPoseEstimate import FingerPoseEstimate
from pose.DeterminePositions import create_known_finger_poses, determine_position, get_position_name_with_pose_id
import operator

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

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

known_finger_poses = create_known_finger_poses()

# Create a hand landmarker instance with the video mode:
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO)
with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
        frame1 = cv2.resize(frame, (640, 480)) 
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
        hand_landmarker_result = landmarker.detect_for_video(mp_image, int(timestamp))
		
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
            score_label = predict_by_geometry([landmarks], known_finger_poses, 0.45)
            print(score_label)
        
