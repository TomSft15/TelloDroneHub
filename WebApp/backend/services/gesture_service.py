import cv2
import mediapipe as mp
import time
import threading
import logging
from services.drone_service import DroneService

logger = logging.getLogger(__name__)

class GestureService:
    """Service pour gérer la détection et le traitement des gestes"""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(GestureService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisation du service de reconnaissance gestuelle"""
        if self._initialized:
            return
            
        self._initialized = True
        self.drone_service = DroneService()
        self.is_running = False
        self.detection_thread = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 3.0  # Temps de refroidissement entre les gestes (en secondes)
        
        # Initialisation de MediaPipe pour la détection des mains
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Définition des gestes et leurs commandes associées
        self.gesture_commands = {
            'takeoff': 'takeoff',            # Main ouverte (5 doigts) = décollage
            'land': 'land',                  # Poing fermé = atterrissage
            'monte': 'moveUp',               # Pouce en position la plus haute = monter
            'descend': 'moveDown',           # Pouce en position la plus basse = descendre
            'flip_left': 'flipLeft',         # Index levé = looping à gauche
            'flip_right': 'flipRight'        # Index et majeur levés = looping à droite
        }
    
    def start_gesture_detection(self):
        """Démarre la détection des gestes"""
        if self.is_running:
            return True, "La détection des gestes est déjà active"
        
        if not self.drone_service.connected or not self.drone_service.drone:
            return False, "Le drone n'est pas connecté"
        
        try:
            self.is_running = True
            self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
            self.detection_thread.start()
            logger.info("Détection des gestes démarrée")
            return True, "Détection des gestes démarrée"
        except Exception as e:
            self.is_running = False
            logger.error(f"Erreur lors du démarrage de la détection des gestes: {e}")
            return False, f"Erreur lors du démarrage de la détection des gestes: {str(e)}"
    
    def stop_gesture_detection(self):
        """Arrête la détection des gestes"""
        if not self.is_running:
            return True, "La détection des gestes est déjà arrêtée"
        
        try:
            self.is_running = False
            # Le thread s'arrêtera naturellement lors de sa prochaine itération
            logger.info("Détection des gestes arrêtée")
            return True, "Détection des gestes arrêtée"
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt de la détection des gestes: {e}")
            return False, f"Erreur lors de l'arrêt de la détection des gestes: {str(e)}"
    
    def _detection_loop(self):
        """Boucle principale de détection des gestes"""
        try:
            with self.mp_hands.Hands(
                max_num_hands=1,
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            ) as hands:
                
                while self.is_running and self.drone_service.connected:
                    try:
                        # Récupérer la frame vidéo du drone
                        frame = self.drone_service.drone.get_frame_read().frame
                        if frame is None:
                            time.sleep(0.1)
                            continue
                        
                        # Convertir la frame pour MediaPipe
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_rgb.flags.writeable = False
                        
                        # Procéder à la détection des mains
                        results = hands.process(frame_rgb)
                        
                        # Si des mains sont détectées
                        if results.multi_hand_landmarks and results.multi_handedness:
                            # Récupérer la latéralité de la main (gauche ou droite)
                            hand_type = results.multi_handedness[0].classification[0].label  # "Left" ou "Right"
                            
                            # Traiter le geste si le temps de refroidissement est écoulé
                            current_time = time.time()
                            if current_time - self.last_gesture_time >= self.gesture_cooldown:
                                hand_landmarks = results.multi_hand_landmarks[0]
                                
                                # Récupérer les positions des landmarks
                                hand_position = []
                                for idx, lm in enumerate(hand_landmarks.landmark):
                                    h, w, c = frame.shape
                                    cx, cy = int(lm.x * w), int(lm.y * h)
                                    hand_position.append([idx, cx, cy])
                                
                                if len(hand_position) == 21:
                                    # Analyser les doigts levés
                                    finger, nbFinger = self._count_fingers_up(hand_position, hand_type)
                                    
                                    # Identifier le geste
                                    gesture = self._handle_sign(finger, hand_position, hand_type)
                                    
                                    # Exécuter la commande correspondante
                                    if gesture:
                                        logger.info(f"Geste détecté: {gesture} (main {hand_type})")
                                        self._execute_gesture_command(gesture)
                                        self.last_gesture_time = current_time
                        
                        # Pause pour économiser les ressources
                        time.sleep(0.1)
                    
                    except Exception as e:
                        logger.error(f"Erreur dans la boucle de détection: {e}")
                        time.sleep(1)  # Pause en cas d'erreur
            
        except Exception as e:
            logger.error(f"Erreur fatale dans la détection des gestes: {e}")
            self.is_running = False
    
    def _count_fingers_up(self, hand_position, handedness="Left"):
        """
        Compte les doigts levés en fonction de la main (gauche ou droite)
        
        Args:
            hand_position: Positions des points de repère de la main
            handedness: Latéralité de la main ("Left" ou "Right")
            
        Returns:
            tuple: (liste des doigts levés, nombre de doigts levés)
        """
        tipIds = [4, 8, 12, 16, 20]
        finger = []
        
        # Vérification du pouce (dépend de la main)
        if handedness == "Left":
            # Main gauche: pouce levé si x du bout > x de la base
            if (hand_position[tipIds[0]][1] > hand_position[tipIds[0] - 1][1]):
                finger.append(1)
            else:
                finger.append(0)
        else:
            # Main droite: pouce levé si x du bout < x de la base
            if (hand_position[tipIds[0]][1] < hand_position[tipIds[0] - 1][1]):
                finger.append(1)
            else:
                finger.append(0)
        
        # Vérification des autres doigts (identique pour les deux mains)
        for id in range(1, 5):
            if (hand_position[tipIds[id]][2] < hand_position[tipIds[id] - 2][2]):
                finger.append(1)
            else:
                finger.append(0)
        
        nbFinger = finger.count(1)
        return finger, nbFinger
    
    def _handle_sign(self, tabFingers, hand_position, handedness="Left"):
        """
        Identifie le geste en fonction des doigts levés et de la position de la main
        
        Args:
            tabFingers: Liste des états des doigts (levés ou non)
            hand_position: Positions des points de repère de la main
            handedness: Latéralité de la main ("Left" ou "Right")
            
        Returns:
            str: Nom du geste détecté ou None si aucun geste reconnu
        """
        # Vérification du pouce en position la plus haute
        is_highest = True
        for i in range(len(hand_position)):
            if hand_position[4][2] > hand_position[i][2]:
                is_highest = False
                break
        if is_highest:
            return "monte"
            
        # Vérification du pouce en position la plus basse
        is_lowest = True
        for i in range(len(hand_position)):
            if hand_position[4][2] < hand_position[i][2]:
                is_lowest = False
                break
        if is_lowest:
            return "descend"
        
        # Vérification de la main ouverte (5 doigts)
        if tabFingers.count(1) == 5:
            return "takeoff"
            
        # Vérification du poing fermé (0 doigt)
        elif tabFingers.count(0) == 5:
            return "land"
            
        # Vérification de l'index levé (flip gauche)
        elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 0 and tabFingers[3] == 0 and tabFingers[4] == 0:
            return "flip_left"
            
        # Vérification de l'index et majeur levés (flip droit)
        elif tabFingers[0] == 0 and tabFingers[1] == 1 and tabFingers[2] == 1 and tabFingers[3] == 0 and tabFingers[4] == 0:
            return "flip_right"
        
        return None
    
    def _execute_gesture_command(self, gesture):
        """
        Exécute la commande associée au geste détecté
        
        Args:
            gesture: Nom du geste détecté
        """
        if not self.drone_service.connected:
            logger.warning("Impossible d'exécuter la commande: drone non connecté")
            return
        
        command = self.gesture_commands.get(gesture)
        if not command:
            logger.warning(f"Aucune commande associée au geste: {gesture}")
            return
        
        try:
            logger.info(f"Exécution de la commande {command} pour le geste {gesture}")
            
            # Exécuter la commande en fonction du type
            if command == 'takeoff':
                self.drone_service.takeoff()
            elif command == 'land':
                self.drone_service.land()
            elif command == 'moveUp':
                self.drone_service.drone.send_rc_control(0, 0, 50, 0)
            elif command == 'moveDown':
                self.drone_service.drone.send_rc_control(0, 0, -50, 0)
            elif command == 'flipLeft':
                self.drone_service.drone.flip_left()
            elif command == 'flipRight':
                self.drone_service.drone.flip_right()
            
            # Pause pour que la commande ait le temps de s'exécuter
            time.sleep(0.5)
            
            # Arrêter le mouvement après les commandes de déplacement
            if command.startswith('move'):
                self.drone_service.drone.send_rc_control(0, 0, 0, 0)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la commande {command}: {e}")
    
    def get_status(self):
        """Retourne l'état actuel de la détection des gestes"""
        return {
            "is_running": self.is_running,
            "cooldown": self.gesture_cooldown,
            "last_gesture_time": self.last_gesture_time,
            "time_until_next": max(0, self.gesture_cooldown - (time.time() - self.last_gesture_time))
        }
    
    def set_cooldown(self, seconds):
        """
        Définit le temps de refroidissement entre les gestes
        
        Args:
            seconds: Temps en secondes
            
        Returns:
            tuple: (succès, message)
        """
        try:
            seconds = float(seconds)
            if seconds < 0.5:
                return False, "Le temps de refroidissement ne peut pas être inférieur à 0.5 seconde"
            if seconds > 10:
                return False, "Le temps de refroidissement ne peut pas être supérieur à 10 secondes"
                
            self.gesture_cooldown = seconds
            return True, f"Temps de refroidissement défini à {seconds} secondes"
        except ValueError:
            return False, "Valeur invalide pour le temps de refroidissement"