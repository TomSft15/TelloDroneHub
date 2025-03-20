import os
import cv2
import face_recognition
import numpy as np
import threading
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('face_recognition_service')

class FaceRecognitionService:
    """Service pour la détection et la reconnaissance de visages."""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(FaceRecognitionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisation du service de reconnaissance faciale"""
        if self._initialized:
            return
            
        self._initialized = True
        self.video_service = None
        self.drone_service = None
        
        # État de la reconnaissance
        self.is_recognition_active = False
        self.recognition_thread = None
        self.stop_recognition = threading.Event()
        
        # Données des personnes reconnues
        self.known_face_encodings = []
        self.known_face_names = []
        self.last_detection = {}  # Pour stocker la dernière détection de chaque personne
        self.current_detections = []  # Personnes actuellement détectées
        
        # Paramètres configurables
        self.settings = {
            'confidence_threshold': 0.4,  # Seuil de confiance pour la reconnaissance
            'detection_interval': 0.5,    # Intervalle entre les détections (secondes)
            'enable_tracking': False,     # Activer le suivi automatique
            'photos_folder': 'pictures_faces',    # Dossier contenant les photos des personnes
            'recognition_scale': 0.25     # Facteur de mise à l'échelle pour accélérer la reconnaissance
        }
        
        # Créer le dossier photos s'il n'existe pas
        os.makedirs(self.settings['photos_folder'], exist_ok=True)
        
        # Tentative de chargement des visages connus
        self.load_known_faces()
    
    def init_services(self, video_service, drone_service):
        """Initialise les services associés"""
        self.video_service = video_service
        self.drone_service = drone_service
    
    def load_known_faces(self):
        """Charge les visages connus depuis le dossier photos"""
        try:
            folder_path = self.settings['photos_folder']
            if not os.path.exists(folder_path):
                logger.info(f"Dossier '{folder_path}' non trouvé. Création du dossier.")
                os.makedirs(folder_path)
                return False, f"Dossier '{folder_path}' créé. Veuillez y ajouter des photos."
            
            # Réinitialise les listes
            self.known_face_encodings = []
            self.known_face_names = []
            
            # Extensions d'image supportées
            extensions = ['.jpg', '.jpeg', '.png']
            
            logger.info(f"Chargement des photos depuis '{folder_path}'...")
            loaded_count = 0
            
            # MODIFICATION: Amélioration de la détection des noms de fichier
            # Parcourir tous les fichiers du dossier
            for filename in os.listdir(folder_path):
                # Vérifier si le fichier est une image
                if any(filename.lower().endswith(ext) for ext in extensions):
                    # Le nom de la personne est extrait du nom du fichier
                    # Si le format est nom_timestamp.jpg, on extrait juste le nom
                    name = os.path.splitext(filename)[0]
                    # Si le nom contient un underscore, on prend tout avant le premier underscore
                    if '_' in name:
                        name = name.split('_')[0]
                    
                    image_path = os.path.join(folder_path, filename)
                    
                    try:
                        # Charger l'image
                        image = face_recognition.load_image_file(image_path)
                        
                        # Extraire les encodages de visage (caractéristiques faciales)
                        face_encodings = face_recognition.face_encodings(image)
                        
                        # Si au moins un visage est détecté dans l'image
                        if len(face_encodings) > 0:
                            # Prendre le premier visage détecté
                            encoding = face_encodings[0]
                            self.known_face_encodings.append(encoding)
                            self.known_face_names.append(name)
                            loaded_count += 1
                            logger.info(f"✅ Photo de '{name}' chargée avec succès.")
                        else:
                            logger.warning(f"⚠️ Aucun visage détecté dans la photo de '{name}'.")
                    except Exception as e:
                        logger.error(f"❌ Erreur lors du chargement de '{filename}': {str(e)}")
            
            if loaded_count > 0:
                logger.info(f"{loaded_count} personnes chargées: {', '.join(self.known_face_names)}")
                return True, f"{loaded_count} personnes chargées avec succès"
            else:
                logger.warning("Aucun visage n'a pu être chargé depuis le dossier de photos.")
                return False, "Aucun visage n'a pu être chargé. Vérifiez que les photos contiennent des visages visibles."
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement des visages connus: {e}")
            return False, f"Erreur lors du chargement des visages: {str(e)}"
    
    def start_face_recognition(self):
        """Démarre le processus de reconnaissance faciale dans un thread séparé"""
        if self.is_recognition_active:
            return True, "La reconnaissance faciale est déjà active"
        
        if len(self.known_face_encodings) == 0:
            success, message = self.load_known_faces()
            if not success:
                return False, f"Impossible de démarrer la reconnaissance: {message}"
        
        if not self.video_service:
            return False, "Service vidéo non initialisé"
        
        try:
            self.stop_recognition.clear()
            self.is_recognition_active = True
            self.current_detections = []
            
            # Démarrer le thread de reconnaissance
            self.recognition_thread = threading.Thread(
                target=self._recognition_loop,
                daemon=True
            )
            self.recognition_thread.start()
            
            logger.info("Reconnaissance faciale démarrée")
            return True, "Reconnaissance faciale démarrée"
        except Exception as e:
            self.is_recognition_active = False
            logger.error(f"Erreur lors du démarrage de la reconnaissance faciale: {e}")
            return False, f"Erreur lors du démarrage: {str(e)}"
    
    def stop_face_recognition(self):
        """Arrête le processus de reconnaissance faciale"""
        if not self.is_recognition_active:
            return True, "La reconnaissance faciale est déjà inactive"
        
        try:
            self.stop_recognition.set()
            
            if self.recognition_thread and self.recognition_thread.is_alive():
                self.recognition_thread.join(timeout=2.0)
            
            self.is_recognition_active = False
            self.current_detections = []
            
            logger.info("Reconnaissance faciale arrêtée")
            return True, "Reconnaissance faciale arrêtée"
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt de la reconnaissance faciale: {e}")
            return False, f"Erreur lors de l'arrêt: {str(e)}"
    
    def get_recognition_status(self):
        """Retourne l'état actuel de la reconnaissance faciale"""
        return {
            "is_active": self.is_recognition_active,
            "known_faces_count": len(self.known_face_names),
            "known_faces": self.known_face_names,
            "current_detections": self.current_detections,
            "settings": self.settings
        }
    
    def update_settings(self, new_settings):
        """Met à jour les paramètres de la reconnaissance faciale"""
        try:
            for key, value in new_settings.items():
                if key in self.settings:
                    # Convertir au type approprié
                    if isinstance(self.settings[key], bool) and not isinstance(value, bool):
                        value = bool(value)
                    elif isinstance(self.settings[key], float) and not isinstance(value, float):
                        value = float(value)
                    
                    self.settings[key] = value
            
            return True, "Paramètres mis à jour avec succès"
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des paramètres: {e}")
            return False, f"Erreur lors de la mise à jour des paramètres: {str(e)}"
    
    def _recognition_loop(self):
        """Boucle principale de reconnaissance faciale"""
        logger.info("Démarrage de la boucle de reconnaissance faciale")
        
        last_recognition_time = 0
        
        while not self.stop_recognition.is_set():
            try:
                current_time = time.time()
                
                # Limiter la fréquence de reconnaissance
                if current_time - last_recognition_time < self.settings['detection_interval']:
                    time.sleep(0.1)  # Courte pause pour éviter de surcharger le CPU
                    continue
                
                # Obtenir l'image actuelle
                if not self.video_service or not hasattr(self.video_service, 'frame'):
                    time.sleep(0.5)
                    continue
                
                frame = self.video_service.frame
                if frame is None:
                    time.sleep(0.5)
                    continue
                
                # Mettre à jour le timestamp de la dernière reconnaissance
                last_recognition_time = current_time
                
                # Effectuer la reconnaissance
                detections = self._process_frame(frame)
                
                # Mettre à jour les détections courantes
                self.current_detections = detections
                
                # Effectuer des actions basées sur les détections (si le suivi est activé)
                if self.settings['enable_tracking'] and self.drone_service and self.drone_service.connected:
                    self._handle_tracking(detections)
                
            except Exception as e:
                logger.error(f"Erreur dans la boucle de reconnaissance faciale: {e}")
                time.sleep(1)  # Pause plus longue en cas d'erreur
        
        logger.info("Boucle de reconnaissance faciale terminée")
    
    def _process_frame(self, frame):
        """Traite une image pour la reconnaissance faciale"""
        if frame is None:
            return []
        
        # Redimensionner pour accélérer le traitement
        scale = self.settings['recognition_scale']
        small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
        
        # Convertir de BGR (OpenCV) à RGB (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Trouver tous les visages dans l'image
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        detections = []
        now = datetime.now()
        
        # Vérifier chaque visage détecté
        for encoding, location in zip(face_encodings, face_locations):
            # Comparer avec les visages connus
            matches = face_recognition.compare_faces(self.known_face_encodings, encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, encoding)
            
            name = "Inconnu"
            confidence = 0
            
            # Si des correspondances sont trouvées
            if len(matches) > 0 and len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    
                    # Log pour déboguer
                    logger.info(f"Détection: {name} avec confiance {confidence:.3f}, seuil: {self.settings['confidence_threshold']}")
                    
                    # Ignorer si la confiance est trop faible
                    if confidence < self.settings['confidence_threshold']:
                        logger.info(f"Détection ignorée: confiance trop faible ({confidence:.3f} < {self.settings['confidence_threshold']})")
                        name = "Inconnu"
                    else:
                        # Enregistrer le moment de la détection
                        self.last_detection[name] = now
            
            # Convertir la position pour correspondre à l'échelle originale
            top, right, bottom, left = [int(coord / scale) for coord in location]
            
            # MODIFICATION: Inclure toutes les détections, même "Inconnu" pour le débogage
            detections.append({
                "name": name,
                "confidence": float(confidence),
                "position": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left
                },
                "timestamp": now.isoformat()
            })
        
        return detections
    
    def _handle_tracking(self, detections):
        """Gère le suivi automatique basé sur les détections"""
        if not detections or not self.drone_service or not self.drone_service.connected:
            return
        
        # Pour l'instant, on suit simplement la première personne détectée
        # Dans une implémentation plus avancée, on pourrait ajouter des priorités
        target = detections[0]
        
        # Obtenir les dimensions du frame
        if not self.video_service or not hasattr(self.video_service, 'frame'):
            return
            
        frame = self.video_service.frame
        if frame is None:
            return
            
        frame_height, frame_width = frame.shape[:2]
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2
        
        # Calculer le centre du visage
        face_left = target['position']['left']
        face_top = target['position']['top']
        face_right = target['position']['right']
        face_bottom = target['position']['bottom']
        
        face_center_x = (face_left + face_right) // 2
        face_center_y = (face_top + face_bottom) // 2
        
        # Calculer l'écart entre le visage et le centre
        delta_x = face_center_x - frame_center_x
        delta_y = face_center_y - frame_center_y
        
        # Zones mortes (deadzone) pour éviter des corrections constantes
        deadzone_x = frame_width * 0.1  # 10% de la largeur
        deadzone_y = frame_height * 0.1  # 10% de la hauteur
        
        # Initialiser les commandes
        yaw_speed = 0    # Rotation horizontale
        up_down_speed = 0  # Mouvement vertical
        
        # Ajuster la rotation horizontale (yaw)
        if abs(delta_x) > deadzone_x:
            yaw_direction = 1 if delta_x > 0 else -1
            yaw_magnitude = min(abs(delta_x) / (frame_width * 0.3), 1.0)  # Normalisation
            yaw_speed = int(20 * yaw_direction * yaw_magnitude)  # Vitesse maximale de 20
        
        # Ajuster le mouvement vertical
        if abs(delta_y) > deadzone_y:
            vertical_direction = -1 if delta_y > 0 else 1  # Inversé car y augmente vers le bas
            vertical_magnitude = min(abs(delta_y) / (frame_height * 0.3), 1.0)  # Normalisation
            up_down_speed = int(20 * vertical_direction * vertical_magnitude)  # Vitesse maximale de 20
        
        # Envoyer les commandes au drone si nécessaire
        if yaw_speed != 0 or up_down_speed != 0:
            try:
                self.drone_service.drone.send_rc_control(0, 0, up_down_speed, yaw_speed)
                logger.debug(f"Tracking: yaw={yaw_speed}, vertical={up_down_speed} pour {target['name']}")
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi des commandes de suivi: {e}")
        
    def capture_face_photo(self, name):
        """Capture une photo d'un visage détecté et l'enregistre"""
        if not self.video_service or not hasattr(self.video_service, 'frame'):
            return False, "Service vidéo non disponible"
        
        frame = self.video_service.frame
        if frame is None:
            return False, "Aucune image disponible"
        
        try:
            # Créer le dossier photos s'il n'existe pas
            os.makedirs(self.settings['photos_folder'], exist_ok=True)
            
            # Générer un nom de fichier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.settings['photos_folder'], f"{name}_{timestamp}.jpg")
            
            # Sauvegarder l'image
            cv2.imwrite(filename, frame)
            
            # Recharger les visages connus
            self.load_known_faces()
            
            return True, f"Photo de {name} sauvegardée sous {filename}"
        except Exception as e:
            logger.error(f"Erreur lors de la capture de la photo: {e}")
            return False, f"Erreur lors de la capture: {str(e)}"
    
    def delete_person(self, name):
        """Supprime toutes les photos d'une personne"""
        if not name:
            return False, "Nom de personne non spécifié"
        
        try:
            folder_path = self.settings['photos_folder']
            deleted_count = 0
            
            # Extensions d'image supportées
            extensions = ['.jpg', '.jpeg', '.png']
            
            # Parcourir tous les fichiers du dossier
            for filename in os.listdir(folder_path):
                # Vérifier si le fichier correspond à la personne
                if any(filename.lower().endswith(ext) for ext in extensions) and filename.startswith(name + "_"):
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)
                    deleted_count += 1
                    logger.info(f"Photo supprimée: {filename}")
            
            # Recharger les visages connus
            self.load_known_faces()
            
            if deleted_count > 0:
                return True, f"{deleted_count} photos de {name} supprimées"
            else:
                return False, f"Aucune photo trouvée pour {name}"
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des photos: {e}")
            return False, f"Erreur lors de la suppression: {str(e)}"
    
    def add_person_from_uploaded_file(self, file_object, person_name):
        """Ajoute une personne à partir d'un fichier téléchargé"""
        if not file_object or not person_name:
            return False, "Fichier ou nom de personne non spécifié"
        
        try:
            # Créer le dossier photos s'il n'existe pas
            os.makedirs(self.settings['photos_folder'], exist_ok=True)
            
            # Générer un nom de fichier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.settings['photos_folder'], f"{person_name}_profile.jpg")
            
            # Sauvegarder le fichier
            file_object.save(filename)
            
            # Vérifier si un visage est détecté dans l'image
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            
            if not face_locations:
                # Supprimer le fichier si aucun visage n'est détecté
                os.remove(filename)
                return False, "Aucun visage détecté dans l'image"
            
            # Recharger les visages connus
            self.load_known_faces()
            
            return True, f"Photo de {person_name} ajoutée avec succès"
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la personne: {e}")
            return False, f"Erreur lors de l'ajout: {str(e)}"