import socket
from gtts import gTTS
import os

# Function to convert text to speech and save it
def texte_en_parole(texte, nom_fichier):
    tts = gTTS(text=texte, lang='fr', slow=False)
    tts.save(nom_fichier)
    os.system(f"start {nom_fichier}")  # Optionally open the audio file

# Client function to receive text and part number, then convert to audio
def client_esclave(adresse_ip, port_pdf=12345, port_audio=5000, esclave_id=1):
    # Connect to receive the part of the PDF
    client_socket_pdf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_pdf.connect((adresse_ip, port_pdf))

    # Receive the text and the part number
    data_recue = client_socket_pdf.recv(8192).decode()
    numero_partie, texte_recu = data_recue.split('\n', 1)
    client_socket_pdf.close()

    # Create an audio file with the part number
    nom_fichier_audio = f"audio_partie_{numero_partie}.mp3"
    texte_en_parole(texte_recu, nom_fichier_audio)

    # Send the audio file to the master
    client_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_audio.connect((adresse_ip, port_audio))

    # Send the part number first, then the audio file
    client_socket_audio.sendall(numero_partie.encode())  # Send part number first
    with open(nom_fichier_audio, 'rb') as fichier_audio:
        client_socket_audio.sendall(fichier_audio.read())  # Send the actual audio file
   
    print(f"Fichier audio '{nom_fichier_audio}' envoyé au maître (partie {numero_partie}).")
    client_socket_audio.close()

if __name__ == "__main__":
    # Call this function for each slave with a unique identifier
    esclave_id = 3  # Change this number for each slave
    client_esclave('192.168.1.22', esclave_id=esclave_id)
