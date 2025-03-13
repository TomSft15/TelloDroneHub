import cv2
import mediapipe as mp
import time

def nbFingerUp(hand_position):
    tipIds = [4, 8, 12, 16, 20]
    finger = []
    if (hand_position[tipIds[0]][1] > hand_position[tipIds[0] - 1][1]):
            finger.append(1)
    else:
        finger.append(0)
    for id in range(1, 5):
        if (hand_position[tipIds[id]][2] < hand_position[tipIds[id] - 2][2]):
            finger.append(1)
        else:
            finger.append(0)
    nbFinger = finger.count(1)
    return finger, nbFinger

def handleSign(tabFingers, hand_position, drone=None, shared_commands=None):
    is_highest = True
    for i in range(len(hand_position)):
        if hand_position[4][2] > hand_position[i][2]:
            is_highest = False
            break
    if is_highest:
        if shared_commands is not None:
            shared_commands.append("monte")
        return
    else:
        is_lowest = True
        for i in range(len(hand_position)):
            if hand_position[4][2] < hand_position[i][2]:
                is_lowest = False
                break
        if is_lowest:
            if shared_commands is not None:
                shared_commands.append("descend")
            return
    
    if tabFingers.count(1) == 5:
        if shared_commands is not None:
            shared_commands.append("takeoff")
    elif tabFingers.count(0) == 5:
        if shared_commands is not None:
            shared_commands.append("land")
    elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 0 and tabFingers[3] == 0 and tabFingers[4] == 0:
        if shared_commands is not None:
            shared_commands.append("flip_left")
    elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 1 and tabFingers[3] == 0 and tabFingers[4] == 0:
        if shared_commands is not None:
            shared_commands.append("flip_right")

def mediapipe_gesture_control(drone=None, hand_position=[], shared_commands=None):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la caméra pour la détection des gestes")
        return

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    last_handle_time = time.time()
    handle_delay = 1.0  # Délai de 1 seconde entre les appels de handleSign

    with mp_hands.Hands(max_num_hands=1,
                        model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erreur lors de la capture de la frame")
                break

            # Conversion de BGR vers RGB pour MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                hand_position = []
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_position.append([id, cx, cy])
                    if (len(hand_position) == 21):
                        finger, nbFinger = nbFingerUp(hand_position)
                
                current_time = time.time()
                if current_time - last_handle_time >= handle_delay:
                    handleSign(finger, hand_position, drone, shared_commands)
                    last_handle_time = current_time

            cv2.imshow("Détection des gestes - MediaPipe", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
