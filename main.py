import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import time
import requests
from groq import Groq
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
load_dotenv()

recogniser = sr.Recognizer()
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)   # Male voice
engine.setProperty("rate", 170)
newsapi = os.environ.get("NEWS_API_KEY")



def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def aiprocess(command):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        
        messages=[{"role": "user", "content": command}]
    )

    return response.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open netflix" in c.lower():
        webbrowser.open("https://netflix.com")
    elif "open flipkart" in c.lower():
        webbrowser.open("https://flipkart.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        url = f"https://newsapi.org/v2/everything?q=India&sortBy=publishedAt&language=en&apiKey={newsapi}"
        r = requests.get(url)
        print(r.json())

        if r.status_code == 200:
            data = r.json()
            print(data)
            articles = data.get("articles", [])

            if not articles:
                speak("No news found.")
            else:
                for article in articles[:5]:
                    title = article["title"]
                    print(title)
                    speak(title)
        else:
            print(r.text)
            speak("Unable to fetch news.")

    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis.....")

    r = sr.Recognizer()
    r.energy_threshold = 300
        

    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)

            word = r.recognize_google(audio)
            word = word.lower().strip()

            print("Recognized:", word)

            if word.lower() == "jarvis":
                print("Before speaking")
                speak("Yes")
                print("After speaking")

                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)

                    print("Listening for command...")
                    audio = r.listen(source, timeout=10, phrase_time_limit=7)

                    command = r.recognize_google(audio)
                    print("Command:", command)

                    processCommand(command)

        except sr.WaitTimeoutError:
            print("No command detected.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")

        except sr.RequestError as e:
            print("Error:", e)