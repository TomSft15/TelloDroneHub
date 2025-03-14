# Configuration de l'application
import os

# Ports
TELLO_PORT = 8889
API_PORT = 5000

# Paramètres vidéo
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

# Intervalle de mise à jour des données du drone (en secondes)
DATA_UPDATE_INTERVAL = 1

# Directory to store known faces
KNOWN_FACES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'known_faces')

# Face recognition parameters
FACE_RECOGNITION_INTERVAL = 10  # Process every Nth frame
MAX_QUEUE_SIZE = 5  # Maximum number of frames to queue for processing