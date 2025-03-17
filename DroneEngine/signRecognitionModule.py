# import cv2
# import mediapipe as mp
# import time

# def nbFingerUp(hand_position):
#     tipIds = [4, 8, 12, 16, 20]
#     finger = []
#     if (hand_position[tipIds[0]][1] > hand_position[tipIds[0] - 1][1]):
#             finger.append(1)
#     else:
#         finger.append(0)
#     for id in range(1, 5):
#         if (hand_position[tipIds[id]][2] < hand_position[tipIds[id] - 2][2]):
#             finger.append(1)
#         else:
#             finger.append(0)
#     nbFinger = finger.count(1)
#     return finger, nbFinger

# def handleSign(tabFingers, hand_position, drone=None, shared_commands=None):
#     is_highest = True
#     for i in range(len(hand_position)):
#         if hand_position[4][2] > hand_position[i][2]:
#             is_highest = False
#             break
#     if is_highest:
#         if shared_commands is not None:
#             shared_commands.append("monte")
#         return
#     else:
#         is_lowest = True
#         for i in range(len(hand_position)):
#             if hand_position[4][2] < hand_position[i][2]:
#                 is_lowest = False
#                 break
#         if is_lowest:
#             if shared_commands is not None:
#                 shared_commands.append("descend")
#             return
    
#     if tabFingers.count(1) == 5:
#         if shared_commands is not None:
#             shared_commands.append("takeoff")
#     elif tabFingers.count(0) == 5:
#         if shared_commands is not None:
#             shared_commands.append("land")
#     elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 0 and tabFingers[3] == 0 and tabFingers[4] == 0:
#         if shared_commands is not None:
#             shared_commands.append("flip_left")
#     elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 1 and tabFingers[3] == 0 and tabFingers[4] == 0:
#         if shared_commands is not None:
#             shared_commands.append("flip_right")

# def mediapipe_gesture_control(drone=None, hand_position=[], shared_commands=None):
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Erreur : Impossible d'ouvrir la caméra pour la détection des gestes")
#         return

#     mp_hands = mp.solutions.hands
#     mp_drawing = mp.solutions.drawing_utils

#     last_handle_time = time.time()
#     handle_delay = 1.0  # Délai de 1 seconde entre les appels de handleSign

#     with mp_hands.Hands(max_num_hands=1,
#                         model_complexity=0,
#                         min_detection_confidence=0.5,
#                         min_tracking_confidence=0.5) as hands:

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Erreur lors de la capture de la frame")
#                 break

#             # Conversion de BGR vers RGB pour MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = hands.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             if results.multi_hand_landmarks:
#                 hand_position = []
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#                 for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
#                     h, w, _ = image.shape
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     hand_position.append([id, cx, cy])
#                     if (len(hand_position) == 21):
#                         finger, nbFinger = nbFingerUp(hand_position)
                
#                 current_time = time.time()
#                 if current_time - last_handle_time >= handle_delay:
#                     handleSign(finger, hand_position, drone, shared_commands)
#                     last_handle_time = current_time

#             cv2.imshow("Détection des gestes - MediaPipe", image)
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()
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

def is_thumb_up(hand_position):
    """Vérifie si le pouce est pointé vers le haut"""
    return (hand_position[4][2] < hand_position[3][2] and 
            hand_position[3][2] < hand_position[2][2])

def is_thumb_down(hand_position):
    """Vérifie si le pouce est pointé vers le bas"""
    return (hand_position[4][2] > hand_position[3][2] and 
            hand_position[3][2] > hand_position[2][2])

def is_pointing_left(hand_position):
    """Vérifie si l'index pointe vers la gauche"""
    return hand_position[8][1] < hand_position[5][1]

def is_pointing_right(hand_position):
    """Vérifie si l'index pointe vers la droite"""
    return hand_position[8][1] > hand_position[5][1]

def is_victory_sign(finger):
    """Vérifie si c'est un signe V (index et majeur tendus)"""
    return finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0

def is_ok_sign(hand_position, finger):
    """Vérifie si c'est un signe OK (pouce et index formant un cercle)"""
    # Vérifier si le pouce et l'index sont proches l'un de l'autre
    distance = ((hand_position[4][1] - hand_position[8][1])**2 + 
                (hand_position[4][2] - hand_position[8][2])**2)**0.5
    
    # Si le pouce est levé, l'index est levé et ils sont proches
    return finger[0] == 1 and finger[1] == 1 and distance < 0.1

def is_rock_sign(finger):
    """Vérifie si c'est un signe rock (pouce et auriculaire tendus)"""
    return finger[0] == 1 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 1

def handleSign(finger, hand_position, drone=None, shared_commands=None):
    # Vérifier si c'est une main ouverte (5 doigts)
    if finger.count(1) == 5:
        if shared_commands is not None:
            shared_commands.append("takeoff")
        return
    
    # Vérifier si c'est un poing fermé
    if finger.count(0) == 5:
        if shared_commands is not None:
            shared_commands.append("land")
        return
    
    # Vérifier si le pouce est pointé vers le haut
    if is_thumb_up(hand_position) and finger.count(1) == 1 and finger[0] == 1:
        if shared_commands is not None:
            shared_commands.append("monte")
        return
    
    # Vérifier si le pouce est pointé vers le bas
    if is_thumb_down(hand_position) and finger.count(1) == 1 and finger[0] == 1:
        if shared_commands is not None:
            shared_commands.append("descend")
        return
    
    # Vérifier si c'est un signe V (avancer)
    if is_victory_sign(finger):
        if shared_commands is not None:
            shared_commands.append("avance")
        return
    
    # Vérifier si c'est un signe OK (reculer)
    if is_ok_sign(hand_position, finger):
        if shared_commands is not None:
            shared_commands.append("recule")
        return
    
    # Vérifier si l'index pointe à gauche
    if finger.count(1) == 1 and finger[1] == 1 and is_pointing_left(hand_position):
        if shared_commands is not None:
            shared_commands.append("gauche")
        return
    
    # Vérifier si l'index pointe à droite
    if finger.count(1) == 1 and finger[1] == 1 and is_pointing_right(hand_position):
        if shared_commands is not None:
            shared_commands.append("droite")
        return
    
    # Vérifier si l'index est pointé vers le haut (vol stationnaire)
    if finger.count(1) == 1 and finger[1] == 1:
        if shared_commands is not None:
            shared_commands.append("hover")
        return
    
    # Vérifier si c'est un signe rock (looping avant)
    if is_rock_sign(finger):
        if shared_commands is not None:
            shared_commands.append("flip_forward")
        return
    
    # Gestes originaux (conservés pour compatibilité)
    if finger[0] == 0 and finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
        if shared_commands is not None:
            shared_commands.append("flip_left")
        return
    elif finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0:
        if shared_commands is not None:
            shared_commands.append("flip_right")
        return

def mediapipe_gesture_control(drone=None, hand_position=[], shared_commands=None):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la caméra pour la détection des gestes")
        return

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    last_handle_time = time.time()
    handle_delay = 3.0  # Délai de 3 secondes entre les appels de handleSign
    
    # Flag pour contrôler l'exécution du thread
    running = True

    with mp_hands.Hands(max_num_hands=1,
                        model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:

        while running:
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
                
                # Afficher le temps restant avant le prochain geste
                time_remaining = max(0, handle_delay - (current_time - last_handle_time))
                cv2.putText(image, f"Cooldown: {time_remaining:.1f}s", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Détection des gestes - MediaPipe", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                running = False
                break

    cap.release()
    cv2.destroyAllWindows()