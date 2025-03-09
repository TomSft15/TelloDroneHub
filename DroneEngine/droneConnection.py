from djitellopy import Tello
import logging

def drone_connection():
    # Initialisation du drone
    drone = Tello()
    Tello.LOGGER.setLevel(logging.DEBUG)

    # Connexion au drone
    print("Connexion au drone Tello en cours...")
    drone.connect(wait_for_state=False)

    print("yoooo")
    # Vérification du niveau de batterie

    return drone