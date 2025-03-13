class DroneData:
    """Classe représentant les données télémétriques du drone"""
    
    def __init__(self):
        self.battery = 0
        self.temperature = 0
        self.flight_time = 0
        self.height = 0
        self.speed = 0
        self.signal = 0
        
    def to_dict(self):
        """Convertit les données en dictionnaire"""
        return {
            "battery": self.battery,
            "temperature": self.temperature,
            "flight_time": self.flight_time,
            "height": self.height,
            "speed": self.speed,
            "signal": self.signal
        }
    
    def update_from_drone(self, drone):
        """Met à jour les données à partir de l'objet drone"""
        try:
            self.battery = drone.get_battery()
            self.temperature = drone.get_temperature()
            self.flight_time = drone.get_flight_time()
            self.height = drone.get_height()
            self.speed = drone.get_speed_x()
            self.signal = 100  # À remplacer par la vraie valeur si disponible
            return True
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return False