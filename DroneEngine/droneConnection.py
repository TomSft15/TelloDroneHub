from djitellopy import Tello
import logging

def drone_connection():
    # Initialisation du drone
    drone = Tello()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('djitellopy').setLevel(logging.WARNING)
    # Tello.LOGGER.setLevel(logging.INFO)

    # Connexion au drone
    print("Connexion au drone Tello en cours...")
    drone.connect()

    # Vérification du niveau de batterie
    battery_level = drone.get_battery()
    print(f"Niveau de batterie : {battery_level}%")
     
    return drone