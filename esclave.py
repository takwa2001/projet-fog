from gtts import gTTS
import os

# Texte à convertir en audio
texte = "Si un seul PC travaille seul, il mettra beaucoup plus de temps pour convertir un PDF volumineux en audio, prenant environ 418 secondes"

# Création de l'objet gTTS avec le texte, langue, et vitesse
tts = gTTS(text=texte, lang='fr', slow=False)

# Sauvegarde de l'audio dans un fichier MP3
tts.save("audio_output.mp3")

# Optionnel : Lecture de l'audio directement après la conversion (Windows)
os.system("start audio_output.mp3")
