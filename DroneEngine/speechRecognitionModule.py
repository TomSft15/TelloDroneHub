import speech_recognition as sr

# ✅ Liste des commandes attendues (en français)
COMMANDS = [
    "décollage", "atterrissage", "avance", "recule",
    "gauche", "droite", "monte", "descends",
    "tourner à gauche", "tourner à droite",
    "lopping à gauche", "lopping à droite", "lopping en avant", "lopping en arrière",
    "stoppe"
]

def speechToText():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Parlez maintenant...")
        try:
            # 🎙️ Écoute avec un timeout rapide
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
            
            # ✅ Reconnaissance vocale en français
            command = recognizer.recognize_google(audio, language='fr-FR').lower()
            print(f"🎤 Vous avez dit : {command}")

            # ✅ Comparaison rapide avec les commandes attendues
            if command in COMMANDS:
                print(f"✅ Commande reconnue : {command}")
                return command
            else:
                print("❌ Désolé, commande non reconnue.")
        except sr.WaitTimeoutError:
            print("⏳ Temps écoulé. Aucun son détecté.")
        except sr.UnknownValueError:
            print("❌ Audio incompréhensible.")
        except sr.RequestError as e:
            print(f"🚨 Erreur avec le service de reconnaissance : {e}")
    return None

def main():
    while True:
        speechToText()

if __name__ == "__main__":
    main()
