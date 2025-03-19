import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
from djitellopy import Tello

def reconnaissance_personne_drone(dossier_photos="photos"):
    """
    Reconnaît les personnes devant la caméra du drone Tello en utilisant des photos de référence.
    
    Args:
        dossier_photos (str): Chemin vers le dossier contenant les photos des personnes à reconnaître
    """
    # Vérifier si le dossier existe
    if not os.path.exists(dossier_photos):
        print(f"Erreur: Le dossier '{dossier_photos}' n'existe pas.")
        print(f"Création du dossier '{dossier_photos}'...")
        os.makedirs(dossier_photos)
        print(f"Veuillez ajouter des photos dans le dossier '{dossier_photos}' et relancer le programme.")
        return
    
    # Charger les visages connus depuis le dossier de photos
    visages_connus = []
    noms_connus = []
    extensions = ['.jpg', '.jpeg', '.png']
    
    print(f"Chargement des photos depuis '{dossier_photos}'...")
    
    # Parcourir tous les fichiers du dossier
    for fichier in os.listdir(dossier_photos):
        # Vérifier si le fichier est une image
        if any(fichier.lower().endswith(ext) for ext in extensions):
            # Le nom de la personne est le nom du fichier sans l'extension
            nom = os.path.splitext(fichier)[0]
            chemin_image = os.path.join(dossier_photos, fichier)
            
            try:
                # Charger l'image
                image = face_recognition.load_image_file(chemin_image)
                
                # Extraire les encodages de visage (caractéristiques faciales)
                encodages = face_recognition.face_encodings(image)
                
                # Si au moins un visage est détecté dans l'image
                if len(encodages) > 0:
                    # Prendre le premier visage détecté
                    encodage = encodages[0]
                    visages_connus.append(encodage)
                    noms_connus.append(nom)
                    print(f"✅ Photo de '{nom}' chargée avec succès.")
                else:
                    print(f"⚠️ Aucun visage détecté dans la photo de '{nom}'.")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de '{fichier}': {str(e)}")
    
    # Vérifier si des visages ont été chargés
    if not visages_connus:
        print("Aucun visage n'a pu être chargé depuis le dossier de photos.")
        print("Assurez-vous que les photos contiennent des visages clairement visibles.")
        return
    
    print(f"\n{len(visages_connus)} personnes chargées: {', '.join(noms_connus)}")
    
    # Initialiser le drone Tello
    print("Connexion au drone Tello...")
    drone = Tello()
    
    try:
        # Connexion au drone
        drone.connect()
        battery = drone.get_battery()
        print(f"Batterie: {battery}%")
        
        # Démarrer le streaming vidéo
        print("Démarrage du flux vidéo...")
        drone.streamon()
        
        print("Démarrage de la reconnaissance faciale sur le flux vidéo du drone...")
        
        derniere_detection = {}
        
        while True:
            # Capturer l'image du drone
            frame = drone.get_frame_read().frame
            if frame is None:
                print("Erreur de capture vidéo du drone.")
                time.sleep(0.1)
                continue
                
            # Réduire la taille de l'image pour accélérer le traitement
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convertir l'image de BGR (OpenCV) à RGB (face_recognition)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Trouver tous les visages dans l'image actuelle
            emplacements_visages = face_recognition.face_locations(rgb_small_frame)
            encodages_visages = face_recognition.face_encodings(rgb_small_frame, emplacements_visages)
            
            noms_visages = []
            maintenant = datetime.now()
            
            # Vérifier chaque visage détecté
            for encodage_visage, emplacement_visage in zip(encodages_visages, emplacements_visages):
                # Comparer avec les visages connus
                correspondances = face_recognition.compare_faces(visages_connus, encodage_visage)
                
                # Calculer les distances pour trouver la meilleure correspondance
                distances_visage = face_recognition.face_distance(visages_connus, encodage_visage)
                meilleur_match_index = np.argmin(distances_visage)
                
                nom = "Inconnu"
                confiance = 0
                
                # Si une correspondance est trouvée
                if len(correspondances) > 0 and correspondances[meilleur_match_index]:
                    nom = noms_connus[meilleur_match_index]
                    confiance = 1 - distances_visage[meilleur_match_index]
                    
                    # Enregistrer le moment de la détection
                    derniere_detection[nom] = maintenant
                
                noms_visages.append((nom, confiance))
            
            # Afficher les résultats
            for (top, right, bottom, left), (nom, confiance) in zip(emplacements_visages, noms_visages):
                # Redimensionner les coordonnées du visage
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Dessiner un cadre autour du visage
                couleur = (0, 0, 255)  # Rouge pour inconnu
                if nom != "Inconnu":
                    # Couleur basée sur la confiance (vert pour confiance élevée)
                    intensite = int(255 * confiance)
                    couleur = (0, intensite, 255 - intensite)
                
                cv2.rectangle(frame, (left, top), (right, bottom), couleur, 2)
                
                # Ajouter le nom et le niveau de confiance
                texte = nom
                if nom != "Inconnu":
                    texte = f"{nom} ({confiance*100:.1f}%)"
                
                # Fond pour le texte
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), couleur, cv2.FILLED)
                cv2.putText(frame, texte, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            # Afficher la liste des personnes reconnues
            y_offset = 30
            cv2.putText(frame, "Personnes reconnues:", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            personnes_presentes = []
            for nom in noms_connus:
                if nom in derniere_detection and (maintenant - derniere_detection[nom]).total_seconds() < 5:
                    personnes_presentes.append(nom)
                    y_offset += 30
                    cv2.putText(frame, f"- {nom}", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if not personnes_presentes:
                y_offset += 30
                cv2.putText(frame, "- Aucune personne reconnue", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Afficher le nombre de visages détectés
            cv2.putText(frame, f"Visages détectés: {len(emplacements_visages)}", (10, frame.shape[0] - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Afficher la batterie du drone
            battery_text = f"Batterie: {drone.get_battery()}%"
            cv2.putText(frame, battery_text, (frame.shape[1] - 150, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Afficher l'image résultante
            cv2.imshow('Reconnaissance Faciale - Drone Tello', frame)
            
            # Quitter avec 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        print(f"Erreur lors de la communication avec le drone: {str(e)}")
    
    finally:
        # Libérer les ressources
        print("Arrêt du streaming vidéo...")
        drone.streamoff()
        print("Déconnexion du drone...")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import time
    reconnaissance_personne_drone()