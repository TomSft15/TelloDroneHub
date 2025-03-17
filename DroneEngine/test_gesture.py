import cv2
import mediapipe as mp
import time

def nbFingerUp(hand_position, handedness="Left"):
    tipIds = [4, 8, 12, 16, 20]
    finger = []
    
    # Détection du pouce (différente selon la main)
    if handedness == "Left":
        # Main gauche: le pouce est levé si le x du bout est plus grand que le x de la base
        if (hand_position[tipIds[0]][1] > hand_position[tipIds[0] - 1][1]):
            finger.append(1)
        else:
            finger.append(0)
    else:
        # Main droite: le pouce est levé si le x du bout est plus petit que le x de la base
        if (hand_position[tipIds[0]][1] < hand_position[tipIds[0] - 1][1]):
            finger.append(1)
        else:
            finger.append(0)
    
    # Pour les autres doigts (identique pour les deux mains)
    for id in range(1, 5):
        if (hand_position[tipIds[id]][2] < hand_position[tipIds[id] - 2][2]):
            finger.append(1)
        else:
            finger.append(0)
    
    nbFinger = finger.count(1)
    return finger, nbFinger

def handleSign(tabFingers, hand_position, shared_commands, handedness="Left"):
    # Vérification du pouce le plus haut ou le plus bas
    is_highest = True
    for i in range(len(hand_position)):
        if hand_position[4][2] > hand_position[i][2]:
            is_highest = False
            break
    if is_highest:
        if shared_commands is not None:
            shared_commands.append("monte")
            print("monte")
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
                print("descend")
            return
    
    # Vérification des gestes basés sur le nombre de doigts levés
    if tabFingers.count(1) == 5:  # Main ouverte
        if shared_commands is not None:
            shared_commands.append("takeoff")
            print("takeoff")
    elif tabFingers.count(0) == 5:  # Poing fermé
        if shared_commands is not None:
            shared_commands.append("land")
            print("land")
    elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 0 and tabFingers[3] == 0 and tabFingers[4] == 0:
        if shared_commands is not None:
            shared_commands.append("flip_left")
            print("flip_left")
    elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 1 and tabFingers[3] == 0 and tabFingers[4] == 0:
        if shared_commands is not None:
            shared_commands.append("flip_right")
            print("flip_right")

def test_gesture_recognition():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la caméra pour la détection des gestes")
        return

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    last_handle_time = time.time()
    handle_delay = 2.0  # Délai de 2 secondes entre les appels de handleSign
    
    # Liste pour simuler les shared_commands
    shared_commands = []

    with mp_hands.Hands(max_num_hands=1,
                        model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:

        print("Test de reconnaissance de gestes démarré!")
        print("Gestes reconnus : 'takeoff', 'land', 'monte', 'descend', 'flip_left', 'flip_right'")
        print("Appuyez sur 'q' pour quitter")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erreur lors de la capture de la frame")
                break
                
            # Flip horizontal pour effet miroir
            frame = cv2.flip(frame, 1)

            # Conversion de BGR vers RGB pour MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks and results.multi_handedness:
                # Récupération de la latéralité de la main
                hand_type = results.multi_handedness[0].classification[0].label  # "Left" ou "Right"
                
                # Affichage de la latéralité sur l'image
                hand_text = f"Main: {hand_type}"
                cv2.putText(image, hand_text, (10, 110), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                
                # Récupération des landmarks
                hand_position = []
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_position.append([id, cx, cy])
                    if (len(hand_position) == 21):
                        finger, nbFinger = nbFingerUp(hand_position, hand_type)
                        
                        # Affichage des doigts levés sur l'image
                        fingers_text = f"Doigts: {finger}"
                        cv2.putText(image, fingers_text, (10, 150), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                current_time = time.time()
                if current_time - last_handle_time >= handle_delay:
                    # Vider la liste de commandes avant chaque détection
                    shared_commands.clear()
                    
                    # Appeler handleSign avec la latéralité
                    handleSign(finger, hand_position, shared_commands, hand_type)
                    
                    last_handle_time = current_time
            
            # Afficher le temps restant avant le prochain geste
            time_remaining = max(0, handle_delay - (time.time() - last_handle_time))
            cv2.putText(image, f"Cooldown: {time_remaining:.1f}s", (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Afficher la dernière commande détectée
            if shared_commands:
                cmd_text = f"Commande: {shared_commands[-1]}"
                cv2.putText(image, cmd_text, (10, 70), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Test Détection de Gestes", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_gesture_recognition()