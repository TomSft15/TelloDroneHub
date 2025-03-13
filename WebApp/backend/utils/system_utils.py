import socket
import subprocess
import sys
from config import TELLO_PORT

def check_port_in_use(port):
    """Vérifie si le port spécifié est déjà utilisé"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.bind(('', port))
        sock.close()
        return False  # Port disponible
    except OSError:
        return True  # Port déjà utilisé

def check_for_existing_processes():
    """Vérifie si des processus utilisent déjà le port du drone"""
    try:
        if sys.platform == "linux" or sys.platform == "darwin":
            output = subprocess.check_output(["lsof", f"-i:{TELLO_PORT}"]).decode()
            if output:
                print(f"Port {TELLO_PORT} déjà utilisé. Veuillez fermer les applications utilisant ce port.")
                print(output)
                return True
        elif sys.platform == "win32":
            output = subprocess.check_output(["netstat", "-ano"]).decode()
            if str(TELLO_PORT) in output:
                print(f"Port {TELLO_PORT} déjà utilisé. Veuillez fermer les applications utilisant ce port.")
                return True
    except:
        # Si la commande échoue, continuez
        pass
    return False