import PyPDF2
from pydub import AudioSegment
from gtts import gTTS
import time  # Import the time module to measure execution time

# Function to read the text from a PDF file
def lire_pdf(nom_fichier_pdf):
    texte_total = ""
    with open(nom_fichier_pdf, "rb") as fichier_pdf:
        lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
        for page in lecteur_pdf.pages:
            texte_total += page.extract_text() + "\n"
    return texte_total

# Function to convert text to audio using gTTS and save it as an mp3 file
def convertir_texte_en_audio(texte):
    tts = gTTS(texte, lang='fr')
    audio_file = 'audio_complet.mp3'
    tts.save(audio_file)
    print(f"Audio généré et sauvegardé sous '{audio_file}'.")
    return audio_file

# Main function to process PDF and convert to audio
def traiter_pdf_et_audio(nom_fichier_pdf):
    # Read the PDF file
    texte = lire_pdf(nom_fichier_pdf)
    
    # Convert the entire text to audio
    fichier_audio = convertir_texte_en_audio(texte)
    
    # Return the audio file name
    return fichier_audio

if __name__ == "__main__":
    nom_fichier_pdf = r"C:\Users\Copytop\Downloads\belles_histoires.pdf"  # Path to the PDF file
    
    # Start the timer
    start_time = time.time()
    
    # Execute the process
    traiter_pdf_et_audio(nom_fichier_pdf)
    
    # Stop the timer and calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Temps d'exécution total: {execution_time:.2f} secondes")
