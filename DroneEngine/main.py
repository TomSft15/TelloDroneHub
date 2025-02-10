from droneConnection import drone_connection
from keyControl import key_control
import pygame as py
import time

def init_pygame():
    py.init()
    py.display.set_mode((360, 240))

def main():
    drone = drone_connection()
    init_pygame()
    
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
- p : Arrêt d'urgence
- m : Quitter le programme
""")
    
    while True:
        tabControl = key_control(drone)
        drone.send_rc_control(tabControl[0], tabControl[1], tabControl[2], tabControl[3])
    
if __name__ == "__main__":
    main()