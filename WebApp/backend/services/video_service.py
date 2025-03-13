import threading
import time
import cv2
import numpy as np
from config import VIDEO_WIDTH, VIDEO_HEIGHT
from services.drone_service import DroneService

class VideoService:
    """Service pour gérer le flux vidéo du drone"""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(VideoService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisation du service vidéo"""
        if self._initialized:
            return
            
        self._initialized = True
        self.drone_service = DroneService()
        self.frame = None
        self.frame_lock = threading.Lock()
        self._video_thread = None
        self._streaming = False
    
    def start_video_stream(self):
        """Démarre le streaming vidéo depuis le drone"""
        if self._streaming:
            return True, "Streaming vidéo déjà actif"
        
        if not self.drone_service.connected or not self.drone_service.drone:
            return False, "Drone non connecté"
        
        try:
            self.drone_service.drone.streamon()
            self._streaming = True
            
            # Démarrer le thread de capture vidéo
            self._video_thread = threading.Thread(target=self._capture_video, daemon=True)
            self._video_thread.start()
            
            return True, "Streaming vidéo démarré"
        except Exception as e:
            return False, f"Erreur lors du démarrage du streaming: {str(e)}"
    
    def stop_video_stream(self):
        """Arrête le streaming vidéo"""
        if not self._streaming:
            return True, "Streaming vidéo déjà arrêté"
        
        try:
            if self.drone_service.connected and self.drone_service.drone:
                self.drone_service.drone.streamoff()
            
            self._streaming = False
            
            return True, "Streaming vidéo arrêté"
        except Exception as e:
            return False, f"Erreur lors de l'arrêt du streaming: {str(e)}"
    
    def _capture_video(self):
        """Capture les images du flux vidéo en arrière-plan"""
        while self._streaming and self.drone_service.connected:
            try:
                current_frame = self.drone_service.drone.get_frame_read().frame
                if current_frame is not None:
                    with self.frame_lock:
                        self.frame = current_frame.copy()
                        self.frame = cv2.resize(self.frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            except Exception as e:
                print(f"Erreur lors de la capture vidéo: {e}")
                time.sleep(0.1)
    
    def generate_frames(self):
        """Générateur qui produit les images pour le streaming MJPEG"""
        while True:
            # Si pas de connexion ou pas d'image, générer une image "Pas de signal"
            if not self.drone_service.connected or self.frame is None:
                no_signal = self._create_no_signal_frame()
                ret, buffer = cv2.imencode('.jpg', no_signal)
                if ret:
                    yield (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                time.sleep(0.5)
                continue
            
            # Sinon, envoyer l'image actuelle
            with self.frame_lock:
                if self.frame is None:
                    time.sleep(0.1)
                    continue
                
                ret, buffer = cv2.imencode('.jpg', self.frame)
                if not ret:
                    continue
            
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    def _create_no_signal_frame(self):
        """Crée une image 'Pas de signal'"""
        img = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)
        cv2.putText(img, "Pas de signal vidéo", (VIDEO_WIDTH//4, VIDEO_HEIGHT//2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img