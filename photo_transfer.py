import cv2
import os
import time
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

# Configuration
REMOTE_HOST = "192.168.1.10"            # Adresse IP du Raspberry Pi
REMOTE_USER = "hp"                      # Nom d'utilisateur du Raspberry Pi
REMOTE_PASSWORD = "raspberrypi"         # Mot de passe du Raspberry Pi
REMOTE_PATH = "/media/hp/MyMedia USB/ps/ps/images" # Chemin distant exact
PHOTO_INTERVAL = 60                     # Intervalle entre les photos (en secondes)

# Configuration du chemin local pour sauvegarder les images
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "images")
if not os.path.exists(desktop_path):
    os.makedirs(desktop_path)  # Crée le dossier "images" sur le bureau s'il n'existe pas encore

# Initialiser la caméra
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Erreur : Impossible d'accéder à la caméra.")
    exit()

# Créer un client SSH pour se connecter au Raspberry Pi
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

# Dimensions pour redimensionner les images
resize_width, resize_height = 640, 480  # Dimensions choisies pour réduire la taille de l'image

try:
    # Connexion au Raspberry Pi
    ssh.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASSWORD)
    scp = SCPClient(ssh.get_transport())

    while True:
        # Capturer une photo
        ret, frame = camera.read()
        if not ret:
            print("Erreur : Impossible de capturer une image.")
            break

        # Redimensionner l'image pour réduire la taille
        frame_resized = cv2.resize(frame, (resize_width, resize_height))

        # Nom de l'image basé sur la date et l'heure
        label = datetime.now().strftime("photo_%Y%m%d_%H%M%S_%f.jpg")
        local_path = os.path.join(desktop_path, label)  # Chemin complet de l'image locale

        # Enregistrer la photo redimensionnée localement
        cv2.imwrite(local_path, frame_resized)
        print(f"Photo capturée et sauvegardée (redimensionnée) : {local_path}")

        # Transférer la photo vers le Raspberry Pi
        try:
            scp.put(local_path, remote_path=f"{REMOTE_PATH}/{label}")
            print(f"Photo {label} envoyée vers {REMOTE_HOST}:{REMOTE_PATH}")
        except Exception as e:
            print(f"Erreur : Impossible de transférer la photo {label} - {e}")

        # Supprimer la photo locale après transfert
        try:
            os.remove(local_path)
            if os.path.exists(local_path):
                print(f"Erreur : Le fichier {local_path} n'a pas pu être supprimé.")
            else:
                print(f"Fichier local {local_path} supprimé avec succès.")
        except Exception as e:
            print(f"Erreur : Impossible de supprimer la photo locale {label} - {e}")

        # Attendre l'intervalle défini avant de capturer la prochaine image
        time.sleep(PHOTO_INTERVAL)

except Exception as e:
    print(f"Erreur : {e}")

finally:
    # Nettoyage
    if camera.isOpened():
        camera.release()
    ssh.close()
    print("Programme terminé.")
