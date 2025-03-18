import cv2
import numpy as np
import threading
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('face_tracking')

class FaceTrackingService:
    """Service pour la détection et le suivi de visages pour le drone Tello."""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(FaceTrackingService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisation du service de suivi facial"""
        if self._initialized:
            return
            
        self._initialized = True
        self.is_tracking = False
        self.tracking_thread = None
        self.face_cascade = None
        self.drone_service = None
        self.stop_event = threading.Event()
        
        # Configuration du suivi
        self.tracking_settings = {
            'detection_frequency': 0.2,  # Secondes entre les détections
            'rotation_speed': 20,        # Vitesse de rotation (0-100)
            'vertical_speed': 20,        # Vitesse verticale (0-100)
            'deadzone_x': 50,            # Zone morte de détection horizontale en pixels
            'deadzone_y': 40,            # Zone morte de détection verticale en pixels
            'face_size_min': 50,         # Taille minimale du visage à détecter
        }
        
        # Chargement du classificateur de visages
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if self.face_cascade.empty():
                logger.error("Impossible de charger le classificateur de visages")
                self.face_cascade = None
        except Exception as e:
            logger.error(f"Erreur lors du chargement du classificateur de visages: {e}")
    
    def init_drone_service(self, drone_service):
        """Initialise le service avec une référence au service drone"""
        self.drone_service = drone_service
        
    def start_face_tracking(self):
        """Démarre le suivi de visage"""
        if self.is_tracking:
            return True, "Le suivi de visage est déjà actif"
        
        if not self.face_cascade:
            return False, "Impossible de démarrer le suivi: classificateur de visages non chargé"
        
        if not self.drone_service or not self.drone_service.connected or not self.drone_service.drone:
            return False, "Impossible de démarrer le suivi: drone non connecté"
        
        try:
            # Réinitialiser l'événement d'arrêt
            self.stop_event.clear()
            
            # Démarrer le thread de suivi
            self.is_tracking = True
            self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
            self.tracking_thread.start()
            
            logger.info("Suivi de visage démarré")
            return True, "Suivi de visage démarré"
        except Exception as e:
            self.is_tracking = False
            logger.error(f"Erreur lors du démarrage du suivi de visage: {e}")
            return False, f"Erreur lors du démarrage du suivi: {str(e)}"
    
    def stop_face_tracking(self):
        """Arrête le suivi de visage"""
        if not self.is_tracking:
            return True, "Le suivi de visage est déjà arrêté"
        
        try:
            # Signaler l'arrêt du thread
            self.stop_event.set()
            
            # Attendre que le thread se termine (avec timeout)
            if self.tracking_thread and self.tracking_thread.is_alive():
                self.tracking_thread.join(timeout=1.0)
            
            self.is_tracking = False
            
            # Arrêter tout mouvement du drone
            if self.drone_service and self.drone_service.connected and self.drone_service.drone:
                self.drone_service.drone.send_rc_control(0, 0, 0, 0)
            
            logger.info("Suivi de visage arrêté")
            return True, "Suivi de visage arrêté"
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt du suivi de visage: {e}")
            return False, f"Erreur lors de l'arrêt du suivi: {str(e)}"
    
    def update_settings(self, settings):
        """Met à jour les paramètres de suivi"""
        for key, value in settings.items():
            if key in self.tracking_settings:
                try:
                    # Convertir la valeur au même type que la valeur existante
                    self.tracking_settings[key] = type(self.tracking_settings[key])(value)
                except (ValueError, TypeError):
                    logger.warning(f"Impossible de convertir la valeur de {key}")
        
        return True, "Paramètres mis à jour"
    
    def get_status(self):
        """Retourne l'état actuel du suivi"""
        return {
            "is_tracking": self.is_tracking,
            "settings": self.tracking_settings,
            "face_detected": False  # Pourrait être mis à jour dans la boucle de suivi
        }
    
    def _tracking_loop(self):
        """Boucle principale de suivi de visage"""
        logger.info("Démarrage de la boucle de suivi de visage")
        
        last_detection_time = 0
        is_first_detection = True
        face_detected = False
        
        try:
            while not self.stop_event.is_set() and self.drone_service.connected:
                current_time = time.time()
                
                # Limiter la fréquence de détection
                if current_time - last_detection_time < self.tracking_settings['detection_frequency']:
                    time.sleep(0.01)  # Pause courte pour ne pas surcharger le CPU
                    continue
                
                # Récupérer l'image actuelle
                frame = self.drone_service.drone.get_frame_read().frame
                
                if frame is None:
                    logger.warning("Aucune image reçue du drone")
                    time.sleep(0.1)
                    continue
                
                # Convertir en niveaux de gris pour la détection
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Détecter les visages
                faces = self.face_cascade.detectMultiScale(
                    gray_frame,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(self.tracking_settings['face_size_min'], self.tracking_settings['face_size_min'])
                )
                
                # Si aucun visage n'est détecté
                if len(faces) == 0:
                    logger.debug("Aucun visage détecté")
                    face_detected = False
                    
                    # Si c'est la première itération, ne rien faire
                    if not is_first_detection:
                        self.drone_service.drone.send_rc_control(0, 0, 0, 0)  # Arrêter tout mouvement
                    
                else:
                    # Prendre le plus grand visage détecté (supposé être le plus proche)
                    largest_face = max(faces, key=lambda face: face[2] * face[3])
                    x, y, w, h = largest_face
                    
                    face_detected = True
                    is_first_detection = False
                    
                    # Calculer la position centrale du visage
                    face_center_x = x + w // 2
                    face_center_y = y + h // 2
                    
                    # Calculer le centre de l'image
                    frame_center_x = frame.shape[1] // 2
                    frame_center_y = frame.shape[0] // 2
                    
                    # Calculer l'écart entre le visage et le centre
                    delta_x = face_center_x - frame_center_x
                    delta_y = face_center_y - frame_center_y
                    
                    # Initialiser les vitesses
                    yaw_speed = 0    # Rotation horizontale
                    up_down_speed = 0  # Mouvement vertical
                    
                    # Ajuster la rotation horizontale (yaw)
                    if abs(delta_x) > self.tracking_settings['deadzone_x']:
                        # Si le visage est à droite du centre
                        if delta_x > 0:
                            yaw_speed = self.tracking_settings['rotation_speed']
                        # Si le visage est à gauche du centre
                        else:
                            yaw_speed = -self.tracking_settings['rotation_speed']
                        
                        # Ajuster la vitesse en fonction de la distance au centre
                        # Plus le visage est loin du centre, plus la rotation est rapide
                        yaw_speed = int(yaw_speed * min(abs(delta_x) / 100, 1.0))
                    
                    # Ajuster le mouvement vertical
                    if abs(delta_y) > self.tracking_settings['deadzone_y']:
                        # Si le visage est en dessous du centre (y augmente vers le bas)
                        if delta_y > 0:
                            up_down_speed = -self.tracking_settings['vertical_speed']  # Descendre
                        # Si le visage est au-dessus du centre
                        else:
                            up_down_speed = self.tracking_settings['vertical_speed']  # Monter
                        
                        # Ajuster la vitesse en fonction de la distance au centre
                        up_down_speed = int(up_down_speed * min(abs(delta_y) / 100, 1.0))
                    
                    # Envoyer la commande au drone
                    # Format: lr, fb, ud, yaw (left/right, forward/backward, up/down, rotation)
                    self.drone_service.drone.send_rc_control(0, 0, up_down_speed, yaw_speed)
                    logger.debug(f"Mouvement - Rotation: {yaw_speed}, Vertical: {up_down_speed}")
                
                # Mettre à jour le temps de la dernière détection
                last_detection_time = current_time
                
        except Exception as e:
            logger.error(f"Erreur dans la boucle de suivi de visage: {e}")
        finally:
            # S'assurer que le drone arrête tout mouvement à la fin du suivi
            if self.drone_service and self.drone_service.connected and self.drone_service.drone:
                self.drone_service.drone.send_rc_control(0, 0, 0, 0)
            
            self.is_tracking = False
            logger.info("Boucle de suivi de visage terminée")