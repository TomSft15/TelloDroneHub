from droneConnection import drone_connection
from keyControl import key_control
import pygame as py
import time
from commands import Commands
import cv2
import threading
import os
from datetime import datetime

def init_pygame():
    py.init()
    py.display.set_caption("Tello Drone Controller")
    py.display.set_mode((360, 240))

def stream_video(drone):
    drone.streamon()  # Active le streaming vidéo
    if not os.path.exists("pictures"):
        os.makedirs("pictures")
    while True:
        frame = drone.get_frame_read().frame  # Capture l'image actuelle
        frame = cv2.resize(frame, (640, 480))  # Redimensionne l'image
        cv2.imshow("Tello Camera", frame)  # Affiche l'image

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quitter la vidéo avec 'q'
            break
        elif key == ord('n'):  # 📸 Prendre une photo avec 'n'
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"pictures/photo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)  # Sauvegarde l'image
            print(f"📸 Photo sauvegardée : {filename}")

    drone.streamoff()  # Désactive le streaming
    cv2.destroyAllWindows()  # Ferme la fenêtre vidéo

def main():
    drone = drone_connection()
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
""")
    
    video_thread = threading.Thread(target=stream_video, args=(drone,))
    video_thread.start()

    commandsClass = Commands(drone)
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                print("🚁 Arrêt du programme...")
                running = False

        tabControl = key_control(drone, commandsClass)
        drone.send_rc_control(tabControl[0], tabControl[1], tabControl[2], tabControl[3])

        py.display.update()
        clock.tick(30)
    
    py.quit()
    print("🏁 Programme terminé.")
    
if __name__ == "__main__":
    main()