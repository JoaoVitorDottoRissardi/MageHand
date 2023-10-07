from pose.utils.FingerCurled import FingerCurled
from pose.utils.FingerPosition import FingerPosition
from pose.utils.FingerDataFormation import FingerDataFormation

def determine_position(curled_positions, finger_positions, known_finger_poses, min_threshold):
    obtained_positions = {}
    
    for finger_pose in known_finger_poses:
        score_at = 0.0
        for known_curl, known_curl_confidence, given_curl in \
            zip(finger_pose.curl_position, finger_pose.curl_position_confidence, curled_positions):
                if len(known_curl) == 0:
                    if len(known_curl_confidence) == 1:
                        score_at += known_curl_confidence[0]
                        continue
                
                if given_curl in known_curl:
                    confidence_at = known_curl.index(given_curl)
                    score_at += known_curl_confidence[confidence_at]
                
        for known_position, known_position_confidence, given_position in \
            zip(finger_pose.finger_position, finger_pose.finger_position_confidence, finger_positions):
                if len(known_position) == 0:
                    if len(known_position_confidence) == 1:
                        score_at += known_position_confidence[0]
                        continue
                        
                if given_position in known_position:
                    confidence_at = known_position.index(given_position)
                    score_at += known_position_confidence[confidence_at]
        
        if score_at >= min_threshold:
            obtained_positions[finger_pose.position_name] = score_at
            
    return obtained_positions

def get_position_name_with_pose_id(pose_id, finger_poses):
    for finger_pose in finger_poses:
        if finger_pose.position_id == pose_id:
            return finger_pose.position_name
    return None


def create_known_finger_poses():
    known_finger_poses = []
    
    ####### 1 ThumbsUp
    thumbsUp = FingerDataFormation()
    thumbsUp.position_name = 'ThumbsUp'
    thumbsUp.curl_position = [
        [FingerCurled.NoCurl],   # Thumb
        [FingerCurled.FullCurl, FingerCurled.HalfCurl], # Index
        [FingerCurled.FullCurl, FingerCurled.HalfCurl], # Middle
        [FingerCurled.FullCurl, FingerCurled.HalfCurl], # Ring
        [FingerCurled.FullCurl, FingerCurled.HalfCurl]  # Little
    ]
    thumbsUp.curl_position_confidence = [
        [1.0], # Thumb
        [1.0, 0.5], # Index
        [1.0, 0.5], # Middle
        [1.0, 0.5], # Ring
        [1.0, 0.5]  # Little
    ]
    thumbsUp.finger_position = [
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft, FingerPosition.DiagonalUpRight], # Thumb
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight], # Index
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight], # Middle
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight], # Ring
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight] # Little
    ]
    thumbsUp.finger_position_confidence = [
        [1.0, 0.7, 0.7], # Thumb
        [0.7, 0.7], # Index
        [0.7, 0.7], # Middle
        [0.7, 0.7], # Ring
        [0.7, 0.7]  # Little
    ]
    thumbsUp.position_id = 0
    known_finger_poses.append(thumbsUp)
    
    ####### 2 ThumbsDown
    thumbsDown = FingerDataFormation()
    thumbsDown.position_name = 'ThumbsDown'
    thumbsDown.curl_position = [
        [FingerCurled.NoCurl],   # Thumb
        [FingerCurled.FullCurl, FingerCurled.HalfCurl], # Index
        [FingerCurled.FullCurl, FingerCurled.HalfCurl], # Middle
        [FingerCurled.FullCurl, FingerCurled.HalfCurl], # Ring
        [FingerCurled.FullCurl, FingerCurled.HalfCurl]  # Little
    ]
    thumbsDown.curl_position_confidence = [
        [1.0], # Thumb
        [1.0, 0.5], # Index
        [1.0, 0.5], # Middle
        [1.0, 0.5], # Ring
        [1.0, 0.5]  # Little
    ]
    thumbsDown.finger_position = [
        [FingerPosition.VerticalDown, FingerPosition.DiagonalDownLeft, FingerPosition.DiagonalDownRight], # Thumb
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight], # Index
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight], # Middle
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight], # Ring
        [FingerPosition.HorizontalLeft, FingerPosition.HorizontalRight] # Little
    ]
    thumbsDown.finger_position_confidence = [
        [0.8, 1.0, 1.0], # Thumb
        [0.7, 0.7], # Index
        [0.7, 0.7], # Middle
        [0.7, 0.7], # Ring
        [0.7, 0.7]  # Little
    ]
    thumbsDown.position_id = 1
    known_finger_poses.append(thumbsDown)
   
    ####### 3 Stop
    stop = FingerDataFormation()
    stop.position_name = 'Stop'
    stop.curl_position = [
        [FingerCurled.NoCurl, FingerCurled.HalfCurl],   # Thumb
        [FingerCurled.NoCurl], # Index
        [FingerCurled.NoCurl], # Middle
        [FingerCurled.NoCurl], # Ring
        [FingerCurled.NoCurl]  # Little
    ]
    stop.curl_position_confidence = [
        [0.7, 0.5], # Thumb
        [0.7], # Index
        [0.7], # Middle
        [1.5], # Ring
        [1.5]  # Little
    ]
    stop.finger_position = [
        [FingerPosition.VerticalUp, FingerPosition.HorizontalLeft], # Thumb
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft, FingerPosition.DiagonalUpRight], # Index
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft, FingerPosition.DiagonalUpRight], # Middle
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft, FingerPosition.DiagonalUpRight], # Ring
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft, FingerPosition.DiagonalUpRight] # Little
    ]
    stop.finger_position_confidence = [
        [0.7, 0.5], # Thumb
        [0.7, 0.3, 0.3], # Index
        [0.7, 0.3, 0.3], # Middle
        [0.7, 0.3, 0.3], # Ring
        [0.7, 0.3, 0.3]  # Little
    ]
    stop.position_id = 2
    known_finger_poses.append(stop)
    
    ####### 4 Peace
    peace = FingerDataFormation()
    peace.position_name = 'Peace'
    peace.curl_position = [
        [FingerCurled.FullCurl, FingerCurled.NoCurl],   # Thumb
        [FingerCurled.NoCurl], # Index
        [FingerCurled.NoCurl], # Middle
        [FingerCurled.FullCurl], # Ring
        [FingerCurled.FullCurl]  # Little
    ]
    peace.curl_position_confidence = [
        [0.5, 0.5], # Thumb
        [1.5], # Index
        [1.5], # Middle
        [1.5], # Ring
        [1.5]  # Little
    ]
    peace.finger_position = [
        [FingerPosition.VerticalUp, FingerPosition.HorizontalLeft], # Thumb
        [FingerPosition.DiagonalUpLeft, FingerPosition.VerticalUp], # Index
        [FingerPosition.DiagonalUpRight, FingerPosition.VerticalUp], # Middle
        [FingerPosition.VerticalUp], # Ring
        [FingerPosition.VerticalUp] # Little
    ]
    peace.finger_position_confidence = [
        [0.2, 0.6], # Thumb
        [1.0, 0.8], # Index
        [1.0, 0.8], # Middle
        [0.5], # Ring
        [0.5]  # Little
    ]
    peace.position_id = 3
    known_finger_poses.append(peace)    

    ####### 5 Fist
    fist = FingerDataFormation()
    fist.position_name = 'Fist'
    fist.curl_position = [
        [FingerCurled.FullCurl, FingerCurled.HalfCurl],   # Thumb
        [FingerCurled.FullCurl], # Index
        [FingerCurled.FullCurl], # Middle
        [FingerCurled.FullCurl], # Ring
        [FingerCurled.FullCurl]  # Little
    ]
    fist.curl_position_confidence = [
        [1.0, 0.7], # Thumb
        [1.0], # Index
        [1.0], # Middle
        [1.0], # Ring
        [1.0]  # Little
    ]
    fist.finger_position = [
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft], # Thumb
        [FingerPosition.VerticalUp, FingerPosition.DiagonalUpLeft], # Index
        [FingerPosition.VerticalUp], # Middle
        [FingerPosition.VerticalUp], # Ring
        [FingerPosition.VerticalUp] # Little
    ]
    fist.finger_position_confidence = [
        [1.0, 0.5], # Thumb
        [1.0, 0.3], # Index
        [1.0], # Middle
        [1.0], # Ring
        [1.0]  # Little
    ]
    fist.position_id = 4
    known_finger_poses.append(fist)
    
    return known_finger_poses
