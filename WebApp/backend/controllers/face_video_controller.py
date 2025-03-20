from flask import Response, jsonify
from flask_restx import Namespace, Resource
from services.face_recognition_service import FaceRecognitionService
from services.video_service import VideoService
import cv2
import numpy as np
import time
import threading
from datetime import datetime

# Création du namespace
face_video_ns = Namespace('face_video', description='Flux vidéo avec reconnaissance faciale')

# Initialisation des services
face_recognition_service = FaceRecognitionService()
video_service = VideoService()

# Variable pour stocker la frame traitée par la reconnaissance faciale
processed_frame = None
frame_lock = threading.Lock()
# Dernières détections
last_detections = {}
last_processed_time = 0
processing_interval = 0.2  # Traiter une image toutes les 200ms

@face_video_ns.route('/feed')
class FaceVideoFeed(Resource):
    @face_video_ns.doc(description='Obtenir le flux vidéo avec reconnaissance faciale')
    def get(self):
        """Obtenir le flux vidéo avec reconnaissance faciale intégrée"""
        return Response(generate_face_frames(), 
                      mimetype='multipart/x-mixed-replace; boundary=frame')

def process_frame_with_face_recognition(frame):
    """Traite une frame pour la reconnaissance faciale et dessine les résultats"""
    if frame is None:
        return None
    
    global last_detections, last_processed_time
    
    # Copier la frame pour éviter de modifier l'originale
    processed = frame.copy()
    
    # Vérifier l'état de la reconnaissance faciale
    status = face_recognition_service.get_recognition_status()
    is_active = status["is_active"]
    known_faces = status["known_faces"]
    
    # Obtenir l'heure actuelle
    now = datetime.now()
    
    # Traiter la frame si la reconnaissance est active et si c'est le moment
    current_time = time.time()
    if is_active and (current_time - last_processed_time) >= processing_interval:
        # Récupérer les détections de face_recognition_service
        detections = face_recognition_service.current_detections
        
        # Mettre à jour les dernières détections
        for detection in detections:
            name = detection["name"]
            last_detections[name] = now
        
        # Mettre à jour l'heure du dernier traitement
        last_processed_time = current_time
    
    # Dessiner les résultats sur la frame
    # 1. Dessiner les cadres autour des visages détectés
    if is_active:
        for detection in face_recognition_service.current_detections:
            name = detection["name"]
            confidence = detection["confidence"]
            position = detection["position"]
            
            top, right, bottom, left = position["top"], position["right"], position["bottom"], position["left"]
            
            # Couleur basée sur la confiance (vert pour confiance élevée)
            intensity = int(255 * confidence)
            color = (0, intensity, 255 - intensity)  # BGR
            
            # Dessiner un cadre autour du visage
            cv2.rectangle(processed, (left, top), (right, bottom), color, 2)
            
            # Ajouter le nom et le niveau de confiance
            text = f"{name} ({confidence*100:.1f}%)"
            
            # Fond pour le texte
            cv2.rectangle(processed, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(processed, text, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    
    # 2. Afficher la liste des personnes reconnues
    y_offset = 30
    cv2.putText(processed, "Personnes reconnues:", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Filtrer les détections récentes (moins de 5 secondes)
    recent_detections = {name: time for name, time in last_detections.items() 
                        if (now - time).total_seconds() < 5}
    
    if recent_detections:
        for name in recent_detections:
            y_offset += 30
            cv2.putText(processed, f"- {name}", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        y_offset += 30
        cv2.putText(processed, "- Aucune personne reconnue", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Afficher le nombre de visages détectés
    cv2.putText(processed, f"Visages détectés: {len(face_recognition_service.current_detections)}", 
               (10, processed.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Afficher si la reconnaissance est active
    status_text = "Reconnaissance faciale active" if is_active else "Reconnaissance faciale inactive"
    status_color = (0, 255, 0) if is_active else (0, 0, 255)
    cv2.putText(processed, status_text, (processed.shape[1] - 300, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    return processed

def generate_face_frames():
    """Générateur qui produit les images pour le streaming MJPEG avec reconnaissance faciale"""
    global processed_frame
    
    while True:
        # Si pas de connexion ou pas d'image, générer une image "Pas de signal"
        if not video_service.frame is None:
            # Traiter la frame avec la reconnaissance faciale
            with frame_lock:
                frame = video_service.frame.copy()
                processed = process_frame_with_face_recognition(frame)
            
            if processed is not None:
                # Convertir l'image en JPEG pour le streaming
                ret, buffer = cv2.imencode('.jpg', processed)
                if ret:
                    yield (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
        else:
            # Créer une image "Pas de signal"
            no_signal_img = create_no_signal_frame()
            ret, buffer = cv2.imencode('.jpg', no_signal_img)
            if ret:
                yield (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        # Petite pause pour éviter de surcharger le CPU
        time.sleep(0.03)  # ~30 FPS

def create_no_signal_frame():
    """Crée une image 'Pas de signal'"""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "Pas de signal vidéo", (640//4, 480//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return img

@face_video_ns.route('/status')
class FaceVideoStatus(Resource):
    @face_video_ns.doc(description='Obtenir le statut du flux vidéo de reconnaissance faciale')
    def get(self):
        """Obtenir le statut du flux vidéo de reconnaissance faciale"""
        recent_detections = []
        now = datetime.now()
        
        for name, time in last_detections.items():
            if (now - time).total_seconds() < 5:
                recent_detections.append(name)
        
        return {
            "success": True,
            "recognition_active": face_recognition_service.is_recognition_active,
            "recent_detections": recent_detections,
            "processing_interval": processing_interval
        }