import socket
import time  # Import time module to measure execution time
import threading
import PyPDF2
from pydub import AudioSegment

# Function to split the text into three equal parts
def diviser_texte_en_trois(texte):
    longueur = len(texte)
    partie1 = texte[:longueur // 3]
    partie2 = texte[longueur // 3:2 * longueur // 3]
    partie3 = texte[2 * longueur // 3:]
    return partie1, partie2, partie3

# Function to read the text from a PDF file
def lire_pdf(nom_fichier_pdf):
    texte_total = ""
    with open(nom_fichier_pdf, "rb") as fichier_pdf:
        lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
        for page in lecteur_pdf.pages:
            texte_total += page.extract_text() + "\n"
    return texte_total

# Function to handle receiving audio and store its part number
def recevoir_audio(conn):
    # First, receive the part number (identifier)
    part_number = int(conn.recv(1).decode())
    
    # Then, receive the actual audio file data
    audio_file = f'audio_partie_{part_number}.mp3'  # Name the file based on the part number
    with open(audio_file, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    
    print(f"Fichier audio reçu pour la partie {part_number} et enregistré sous '{audio_file}'")
    conn.close()
    
    return part_number, audio_file

# Function to concatenate audio files in the correct order
def concatener_audio(fichiers_audio):
    audio_concatene = AudioSegment.empty()  # Create an empty audio segment

    # Sort audio files by their part number
    fichiers_audio_tries = sorted(fichiers_audio, key=lambda x: x[0])

    # Concatenate files in the correct order
    for part_number, nom_fichier in fichiers_audio_tries:
        try:
            audio = AudioSegment.from_file(nom_fichier)  # Load the audio file
            audio_concatene += audio  # Add the file to the concatenated segment
            print(f"Ajout de '{nom_fichier}' à la concaténation (partie {part_number}).")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier '{nom_fichier}': {e}")

    # Export the concatenated audio file
    audio_concatene.export("audio_concatene.mp3", format="mp3")
    print("Les fichiers audio ont été concaténés et sauvegardés sous 'audio_concatene.mp3'.")

# Main function for the master server
def serveur_maitre(texte, adresse_ip, port_pdf=12345, port_audio=5000):
    # Record the start time
    start_time = time.time()
    
    # Split the text into three parts
    partie1, partie2, partie3 = diviser_texte_en_trois(texte)
    parties = [partie1, partie2, partie3]
    
    # Create a socket to send PDF parts
    serveur_socket_pdf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket_pdf.bind((adresse_ip, port_pdf))
    serveur_socket_pdf.listen(3)
    print("Serveur en attente de connexions pour l'envoi des parties du PDF...")

    connexions = []
    for i in range(3):
        connexion, adresse_client = serveur_socket_pdf.accept()
        print(f"Connexion établie avec l'esclave {i+1} à {adresse_client}")
        connexions.append((connexion, i+1))  # Store the connection and slave ID
    
    # Send each part and its ID to the respective slaves
    for connexion, esclave_id in connexions:
        # Send the part number and text
        connexion.sendall(f"{esclave_id}\n{parties[esclave_id-1]}".encode())
        connexion.close()

    serveur_socket_pdf.close()

    # Create a socket to receive the audio files
    serveur_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket_audio.bind((adresse_ip, port_audio))
    serveur_socket_audio.listen(3)
    print("Serveur en attente de connexions pour la réception des fichiers audio...")

    fichiers_audio = []  # List to store received audio filenames with part numbers

    # Accept connections to receive audio files
    for i in range(3):
        conn, addr = serveur_socket_audio.accept()
        part_number, fichier_recu = recevoir_audio(conn)  # Receive audio and store with part number
        fichiers_audio.append((part_number, fichier_recu))

    serveur_socket_audio.close()

    # Concatenate the received audio files in the correct order
    concatener_audio(fichiers_audio)

    # Record the end time
    end_time = time.time()

    # Calculate and print the total execution time
    execution_time = end_time - start_time
    print(f"Le processus complet a pris {execution_time:.2f} secondes.")

if __name__ == "__main__":
    nom_fichier_pdf = r"C:\Users\Copytop\Downloads\belles_histoires.pdf"  # Path to the PDF file
    texte = lire_pdf(nom_fichier_pdf)
    serveur_maitre(texte, '192.168.1.22')
