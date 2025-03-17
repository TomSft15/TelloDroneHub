# from droneConnection import drone_connection
# from keyControl import key_control
# from signRecognitionModule import mediapipe_gesture_control
# import pygame as py
# import time
# from commands import Commands
# import cv2
# import threading
# import os
# from datetime import datetime
# import mediapipe as mp
# import base64
# import socketio
# import logging
# logging.basicConfig(level=logging.INFO)


# def init_pygame():
#     py.init()
#     py.display.set_caption("Tello Drone Controller")
#     py.display.set_mode((360, 240))

# def capture_camera():
#     cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

#     if not cap.isOpened():
#         print("Erreur : Impossible d'ouvrir la caméra")
#         return

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Erreur : Impossible de lire le frame")
#             break

#         cv2.imshow("Camera", frame)

#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):  # Quitter la vidéo avec 'q'
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# def stream_video_drone(drone):
#     # Connexion au serveur Socket.IO
#     sio = socketio.Client()
#     try:
#         sio.connect('http://localhost:3000')  # Adapter l'URL si nécessaire
#         print("Connecté au serveur Socket.IO")
#     except Exception as e:
#         print("Erreur de connexion au serveur Socket.IO :", e)
#         return

#     drone.streamon()  # Active le streaming vidéo
#     if not os.path.exists("pictures"):
#         os.makedirs("pictures")
#     while True:
#         frame = drone.get_frame_read().frame  # Capture l'image actuelle
#         frame = cv2.resize(frame, (640, 480))  # Redimensionne l'image

#         # Affiche la frame en local
#         cv2.imshow("Tello Camera", frame)
        
#         # Encodage de la frame en JPEG
#         ret, buffer = cv2.imencode('.jpg', frame)
#         if ret:
#             # Conversion en base64 pour l'envoi via Socket.IO
#             jpg_as_text = base64.b64encode(buffer).decode('utf-8')
#             sio.emit('video_frame', jpg_as_text)

#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):  # Quitter la vidéo avec 'q'
#             break
#         elif key == ord('n'):  # 📸 Prendre une photo avec 'n'
#             timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             filename = f"pictures/photo_{timestamp}.jpg"
#             cv2.imwrite(filename, frame)  # Sauvegarde l'image
#             print(f"📸 Photo sauvegardée : {filename}")

#     drone.streamoff()  # Désactive le streaming
#     sio.disconnect()
#     cv2.destroyAllWindows()  # Ferme la fenêtre vidéo

# def main():
#     drone = drone_connection()  # Décommentez si vous souhaitez connecter le drone
#     init_pygame()
    
#     clock = py.time.Clock()
#     time.sleep(8)
    
#     print("""
# Commandes disponibles :
# - a : Décollage
# - e : Atterrissage
# - z : Avancer
# - s : Reculer
# - q : Aller à gauche
# - d : Aller à droite
# - Flèche haut : Monter
# - Flèche bas : Descendre
# - Flèche gauche : Rotation gauche
# - Flèche droite : Rotation droite
# - t : Front flip
# - g : Back flip
# - f : Left flip
# - h : Right flip
# - i : Speech recognition
# - p : Arrêt d'urgence
# - m : Quitter le programme

# Commandes gestuelles via MediaPipe :
# - Main ouverte (5 doigts étendus) : takeoff (décollage)
# - Main fermée (aucun doigt étendu) : land (atterrissage)
# - Pouce tendu en haut (avec main fermée) : monte (monter)
# - Pouce tendu en bas (avec main fermée) : descend (descendre)
# Appuyez sur 'q' pour quitter la détection gestuelle.
# """)
    
#     hand_position = []
#     shared_commands = []
#     last_command_time = time.time()
#     command_delay = 1.0  # Délai de 1 seconde entre les commandes
    
#     # Lancement de la détection gestuelle dans un thread séparé
#     # gesture_thread = threading.Thread(target=mediapipe_gesture_control, args=(None, hand_position, shared_commands), daemon=True)
#     # gesture_thread.start()
    
#     video_thread = threading.Thread(target=stream_video_drone, args=(drone,))
#     video_thread.start()
    
#     # Si vous souhaitez simplement visualiser le flux de la caméra sans détection, vous pouvez utiliser capture_camera()
#     # capture_camera()
#     # stream_video_drone(drone)
    
#     running = True
#     while running:
#         for event in py.event.get():
#             if event.type == py.QUIT:
#                 print("🚁 Arrêt du programme...")
#                 running = False

#         # Exemple de récupération des commandes clavier (décommentez si vous utilisez le contrôle par touches)
#         tabControl = key_control(drone) #commandsClass)
#         drone.send_rc_control(tabControl[0], tabControl[1], tabControl[2], tabControl[3])
        
#         # Utilisation des commandes partagées
#         current_time = time.time()
#         if shared_commands and (current_time - last_command_time >= command_delay):
#             command = shared_commands.pop(0)
#             print(f"Commande reçue : {command}")
#             last_command_time = current_time
        
#         py.display.update()
#         clock.tick(30)
    
#     py.quit()
#     print("🏁 Programme terminé.")
    
# if __name__ == "__main__":
#     main()
from droneConnection import drone_connection
from keyControl import key_control
from signRecognitionModule import mediapipe_gesture_control
import pygame as py
import time
from commands import Commands
import cv2
import threading
import os
from datetime import datetime
import mediapipe as mp
import base64
import socketio
import logging
logging.basicConfig(level=logging.INFO)


def init_pygame():
    py.init()
    py.display.set_caption("Tello Drone Controller")
    py.display.set_mode((360, 240))

def capture_camera():
    cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la caméra")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire le frame")
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quitter la vidéo avec 'q'
            break

    cap.release()
    cv2.destroyAllWindows()

def stream_video_drone(drone):
    # Connexion au serveur Socket.IO
    sio = socketio.Client()
    try:
        sio.connect('http://localhost:3000')  # Adapter l'URL si nécessaire
        print("Connecté au serveur Socket.IO")
    except Exception as e:
        print("Erreur de connexion au serveur Socket.IO :", e)
        return

    drone.streamon()  # Active le streaming vidéo
    if not os.path.exists("pictures"):
        os.makedirs("pictures")
    while True:
        frame = drone.get_frame_read().frame  # Capture l'image actuelle
        frame = cv2.resize(frame, (640, 480))  # Redimensionne l'image

        # Affiche la frame en local
        cv2.imshow("Tello Camera", frame)
        
        # Encodage de la frame en JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            # Conversion en base64 pour l'envoi via Socket.IO
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            sio.emit('video_frame', jpg_as_text)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quitter la vidéo avec 'q'
            break
        elif key == ord('n'):  # 📸 Prendre une photo avec 'n'
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"pictures/photo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)  # Sauvegarde l'image
            print(f"📸 Photo sauvegardée : {filename}")

    drone.streamoff()  # Désactive le streaming
    sio.disconnect()
    cv2.destroyAllWindows()  # Ferme la fenêtre vidéo

def main():
    # drone = drone_connection()  # Décommentez si vous souhaitez connecter le drone
    init_pygame()
    
    clock = py.time.Clock()
    time.sleep(8)
    
    print("""
Commandes disponibles :
- a : Décollage
- e : Atterrissage
- z : Avancer
- s : Reculer
- q : Aller à gauche
- d : Aller à droite
- Flèche haut : Monter
- Flèche bas : Descendre
- Flèche gauche : Rotation gauche
- Flèche droite : Rotation droite
- t : Front flip
- g : Back flip
- f : Left flip
- h : Right flip
- i : Speech recognition
- p : Arrêt d'urgence
- m : Quitter le programme
- g : Activer/désactiver la reconnaissance gestuelle

Commandes gestuelles via MediaPipe :
- Main ouverte (5 doigts étendus) : takeoff (décollage)
- Main fermée (aucun doigt étendu) : land (atterrissage)
- Pouce tendu en haut (avec main fermée) : monte (monter)
- Pouce tendu en bas (avec main fermée) : descend (descendre)
- Signe V (index et majeur tendus) : avancer
- Signe OK (pouce et index formant un cercle) : reculer
- Index tendu à gauche : déplacement à gauche
- Index tendu à droite : déplacement à droite
- Index pointé vers le haut : vol stationnaire
- Signe rock (pouce et auriculaire tendus) : looping avant

Appuyez sur 'q' pour quitter la détection gestuelle.
""")
    
    hand_position = []
    shared_commands = []
    last_command_time = time.time()
    command_delay = 1.0  # Délai de 1 seconde entre les commandes
    # commandsClass = Commands(drone)
    
    # État initial de la reconnaissance gestuelle
    gesture_recognition_enabled = False
    gesture_thread = None
    
    # video_thread = threading.Thread(target=stream_video_drone, args=(drone,))
    # video_thread.daemon = True
    # video_thread.start()
    
    capture_camera()
    
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                print("🚁 Arrêt du programme...")
                running = False

        # Exemple de récupération des commandes clavier
        # tabControl = key_control(drone, commandsClass)
        # drone.send_rc_control(tabControl[0], tabControl[1], tabControl[2], tabControl[3])
        
        # Activation/désactivation de la reconnaissance gestuelle avec la touche g
        keys = py.key.get_pressed()
        if keys[py.K_g]:
            # Utiliser un délai pour éviter les activations multiples
            current_time = time.time()
            if current_time - last_command_time >= command_delay:
                gesture_recognition_enabled = not gesture_recognition_enabled
                last_command_time = current_time
                
                if gesture_recognition_enabled:
                    print("🖐️ Reconnaissance gestuelle activée")
                    # Lancement de la détection gestuelle dans un thread séparé
                    gesture_thread = threading.Thread(
                        target=mediapipe_gesture_control, 
                        args=(drone, hand_position, shared_commands), 
                        daemon=True
                    )
                    gesture_thread.start()
                else:
                    print("✋ Reconnaissance gestuelle désactivée")
                    # Le thread s'arrêtera naturellement lors de sa prochaine itération
                    gesture_thread = None
        
        # Utilisation des commandes partagées
        current_time = time.time()
        if shared_commands and (current_time - last_command_time >= command_delay):
            command = shared_commands.pop(0)
            print(f"Commande reçue : {command}")
            last_command_time = current_time
        
        py.display.update()
        clock.tick(30)
    
    py.quit()
    print("🏁 Programme terminé.")
    
if __name__ == "__main__":
    main()