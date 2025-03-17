import threading
import time
from config import DATA_UPDATE_INTERVAL, TELLO_PORT
from models.drone_data import DroneData
from utils.system_utils import check_for_existing_processes, check_port_in_use

class DroneService:
    """Service pour gérer la connexion et les commandes du drone"""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(DroneService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisation du service drone"""
        if self._initialized:
            return
            
        self._initialized = True
        self.drone = None
        self.connected = False
        self.drone_data = DroneData()
        self._data_thread = None
    
    def connect(self):
        """Connecte au drone Tello"""
        if self.connected:
            return True, "Drone déjà connecté"
        
        if check_for_existing_processes():
            return False, "Processus existants utilisent déjà le port du drone"
        
        if check_port_in_use(TELLO_PORT):
            return False, f"Le port {TELLO_PORT} est déjà utilisé"
        
        try:
            # Import djitellopy ici pour éviter les erreurs si le module n'est pas installé
            from djitellopy import Tello
            
            # Initialisation du drone
            self.drone = Tello()
            
            # Tentative de connexion
            self.drone.connect()
            self.connected = True
            
            # Démarrer le thread de mise à jour des données
            self._data_thread = threading.Thread(target=self._update_drone_data, daemon=True)
            self._data_thread.start()
            
            return True, "Drone connecté avec succès"
            
        except ImportError:
            return False, "La bibliothèque djitellopy n'est pas installée"
        except Exception as e:
            return False, f"Erreur lors de la connexion au drone: {str(e)}"
    
    def disconnect(self):
        """Déconnecte le drone"""
        if not self.connected:
            return True, "Drone déjà déconnecté"
        
        try:
            # Atterrir si le drone est en vol
            if self.drone.is_flying:
                self.drone.land()
            
            # Arrêter le streaming vidéo s'il est actif
            self.drone.streamoff()
            
            self.connected = False
            self.drone = None
            
            return True, "Drone déconnecté avec succès"
        except Exception as e:
            return False, f"Erreur lors de la déconnexion: {str(e)}"
    
    def _update_drone_data(self):
        """Met à jour les données du drone en arrière-plan"""
        while self.connected and self.drone:
            try:
                self.drone_data.update_from_drone(self.drone)
            except Exception as e:
                print(f"Erreur lors de la mise à jour des données: {e}")
            time.sleep(DATA_UPDATE_INTERVAL)
    
    def get_drone_data(self):
        """Retourne les données actuelles du drone"""
        return self.drone_data.to_dict()
    
    def takeoff(self):
        """Faire décoller le drone"""
        if not self.connected or not self.drone:
            return False, "Drone non connecté"
        try:
            self.drone.takeoff()
            # Pause courte pour laisser le drone se stabiliser initialement
            import time
            time.sleep(0.5)  # Attendre 500ms
            
            # Envoyer une commande de vol stationnaire pour garantir la stabilité
            self.drone.send_rc_control(0, 0, 0, 0)
            
            return True, "Décollage réussi et stabilisation activée"
        except Exception as e:
            return False, f"Erreur lors du décollage: {str(e)}"
    
    def land(self):
        """Commande d'atterrissage"""
        if not self.connected or not self.drone:
            return False, "Drone non connecté"
        try:
            self.drone.land()
            return True, "Atterrissage réussi"
        except Exception as e:
            return False, f"Erreur lors de l'atterrissage: {str(e)}"