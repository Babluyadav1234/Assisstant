
import os
import pyttsx3
import speech_recognition as sr
from openai import OpenAI

# ==============================
# BABLU AI VOICE ASSISTANT
# ==============================

# Connect to OpenAI API
client = OpenAI()

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)


# Speak function
def speak(text):
    print("\n🤖 Bablu AI:", text)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as error:
        print("Voice Error:", error)


# Ask AI function
def ask_ai(question):
    try:
        print("\n⏳ Bablu AI is thinking...")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=question
        )

        answer = response.output_text

        if answer:
            return answer

        return "Sorry, I could not generate an answer."

    except Exception as error:
        print("AI Error:", error)
        return (
            "Sorry, AI se connect nahi ho paya. "
            "API key, internet aur API account check karein."
        )


# Listen to microphone
def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\n🎤 Listening... Ab boliye!")

            recognizer.adjust_for_ambient_noise(
                source, duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        question = recognizer.recognize_google(
            audio,
            language="hi-IN"
        )

        print("🗣️ You:", question)
        return question

    except sr.WaitTimeoutError:
        speak("Aapki awaaz sunai nahi di. Dobara boliye.")
        return ""

    except sr.UnknownValueError:
        speak("Sorry, main aapki baat samajh nahi paya.")
        return ""

    except sr.RequestError as error:
        print("Speech Recognition Error:", error)
        speak("Speech recognition service mein problem hai.")
        return ""

    except Exception as error:
        print("Microphone Error:", error)
        speak("Microphone check karein.")
        return ""


# Main program
def main():
    speak("Hello! Main Bablu AI hoon.")
    speak("Aap mujhse type karke ya bolkar sawal pooch sakte hain.")
    speak("Voice mode ke liye V type karein.")
    speak("Program band karne ke liye exit type karein.")

    while True:
        try:
            question = input(
                "\n⌨️ You (question / V / exit): "
            ).strip()

            if question.lower() == "exit":
                speak("Goodbye! Aapka din shubh ho.")
                break

            # Voice mode
            if question.lower() == "v":
                question = listen()

                if not question:
                    continue

            # Ask AI
            if question:
                answer = ask_ai(question)
                speak(answer)

        except KeyboardInterrupt:
            speak("Bablu AI band ho raha hai. Goodbye!")
            break

        except Exception as error:
            print("Program Error:", error)


# Start program
if __name__ == "__main__":
    main()
