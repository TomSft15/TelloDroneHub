from djitellopy import Tello

def drone_connection():
    # Initialisation du drone
    drone = Tello()

    # Connexion au drone
    print("Connexion au drone Tello en cours...")
    drone.connect()

    # Vérification du niveau de batterie
    battery_level = drone.get_battery()
    print(f"Niveau de batterie : {battery_level}%")

    return drone
