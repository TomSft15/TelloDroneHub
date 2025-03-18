# Projet de contrôle de drone Tello DJI

## Présentation du projet

Ce projet consiste en une application complète pour contrôler un drone Tello DJI via différentes interfaces utilisateur intuitives. L'objectif principal est de proposer plusieurs modes d'interaction avec le drone, notamment par commandes vocales, gestes, et reconnaissance faciale, le tout intégré dans une interface web conviviale.

---

## Fonctionnalités principales

### Contrôle du drone
- **Contrôle par clavier** : Pilotage du drone avec les touches directionnelles et des raccourcis clavier
- **Commandes vocales** : Contrôle du drone par reconnaissance vocale (ex: "décoller", "atterrir", "avancer")
- **Contrôle gestuel** : Détection de gestes de la main pour piloter le drone
- **Suivi facial automatique** : Le drone peut détecter et suivre un visage automatiquement

### Interface utilisateur
- **Tableau de bord** : Visualisation en temps réel des données télémétriques du drone
- **Flux vidéo** : Affichage du flux vidéo de la caméra embarquée du drone
- **Capture de photos** : Possibilité de prendre des photos depuis le drone
- **Personnalisation** : Configuration des contrôles clavier selon les préférences de l'utilisateur

### Autres fonctionnalités
- **Reconnaissance faciale** : Détection et identification de personnes
- **Statistiques de vol** : Suivi de la durée de vol, de la batterie, etc.
- **Mode d'urgence** : Commandes d'urgence pour assurer la sécurité du vol

---

## Architecture technique

### Backend (Python)
- Framework **Flask** pour l'API REST
- **Flask-RESTx** pour la documentation API automatique avec Swagger
- **OpenCV** pour le traitement d'image et la détection faciale
- **Mediapipe** pour la reconnaissance de gestes
- **SpeechRecognition** pour la reconnaissance vocale
- **djitellopy** pour l'interfaçage avec le drone Tello

### Frontend (Vue.js)
- **Vue.js 3** comme framework frontend
- Composants modulaires pour les différents modes de contrôle
- Utilisation de **socket.io** pour la communication en temps réel
- Interface responsive accessible sur ordinateur et mobile

---

## Structure du projet

Le projet est organisé en deux parties principales :

### Backend
- `app.py` : Point d'entrée de l'application Flask
- `controllers/` : Contrôleurs pour les différentes fonctionnalités (drone, vidéo, gestes, etc.)
- `services/` : Logique métier pour le contrôle du drone, traitement vidéo, etc.
- `models/` : Modèles de données
- `utils/` : Utilitaires divers

### Frontend
- `src/components/` : Composants Vue.js réutilisables
- `src/views/` : Vues principales de l'application
- `src/services/` : Services pour l'API et les fonctionnalités frontales
- `src/mixins/` : Fonctionnalités partagées comme les contrôles clavier

---

## Installation et utilisation

### Prérequis
- Python 3.8+ avec pip
- Node.js et yarn
- Un drone Tello DJI
- Une connexion Wi-Fi pour se connecter au drone

### Installation du backend
1. Créer un environnement virtuel Python
2. Installer les dépendances via `pip install -r requirements.txt`
3. Lancer le serveur avec `python app.py`

### Installation du frontend
1. Installer les dépendances via `yarn install`
2. Lancer le serveur de développement avec `yarn serve`

### Connexion au drone
1. Allumer le drone Tello
2. Se connecter au réseau Wi-Fi du drone depuis l'ordinateur
3. Utiliser l'interface "Connecter un drone" dans l'application
4. Une fois connecté, accéder au tableau de bord pour contrôler le drone

---

## Caractéristiques techniques importantes

- API RESTful documentée avec Swagger UI
- Architecture modulaire pour faciliter l'extension
- Implémentation de différents types de contrôle (clavier, voix, geste)
- Mode simulation permettant d'utiliser l'application sans drone
- Conception responsive pour différentes tailles d'écran

---

## Résolution des problèmes courants

1. **Le drone ne se connecte pas** :
   - Vérifiez que vous êtes bien connecté au réseau Wi-Fi du drone
   - Assurez-vous que la batterie du drone est suffisamment chargée
   - Redémarrez le drone et l'application

2. **La reconnaissance vocale ne fonctionne pas** :
   - Vérifiez que votre navigateur supporte l'API Web Speech (Chrome recommandé)
   - Assurez-vous que votre microphone est correctement configuré et autorisé

3. **La détection de gestes n'est pas précise** :
   - Assurez-vous d'être dans un environnement bien éclairé
   - Positionnez-vous à environ 1 mètre de la caméra
   - Effectuez des gestes clairs et distincts

4. **Erreur "Port déjà utilisé"** :
   - Assurez-vous qu'aucun autre programme n'utilise les ports 5000 (backend) ou 8080 (frontend)
   - Redémarrez votre ordinateur pour libérer les ports

---

## Perspectives d'évolution

- Ajout de fonctionnalités de cartographie et navigation GPS
- Amélioration des algorithmes de reconnaissance faciale
- Support de plusieurs drones simultanément
- Mode missions programmées automatiques
- Export des données de vol et intégration avec d'autres applications

Ce projet représente une interface complète entre l'humain et le drone, offrant de multiples modalités d'interaction adaptées à différents cas d'usage, de l'utilisation ludique à des applications plus professionnelles.

---

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## Contact

Pour toute question, suggestion ou problème, veuillez contacter :

- **Thomas Fiancette** (Chef de projet) - [email@example.com]
- **Charles Fassel-Ashley** - [email@example.com]
- **Eliyan Dochev** - [email@example.com]

---

## Remerciements

- Équipe de développement DJI pour le SDK Tello
- Contributeurs des bibliothèques OpenCV, Mediapipe et autres outils open-source utilisés dans ce projet