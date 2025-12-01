
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import os
import requests
from random import choice


engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


opening_text = [
    "Cool, I'm on it sir.",
    "Okay sir, I'm working on it.",
    "Just a second sir."
]

# News API key (replace with your own key from https://newsapi.org/)
NEWS_API_KEY = "your_news_api_key_here"



def speak(text):
    """Convert text to speech."""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()



def greet_user():
    """Greet user according to the time of day."""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning sir!")
    elif 12 <= hour < 16:
        speak("Good Afternoon sir!")
    elif 16 <= hour < 21:
        speak("Good Evening sir!")
    else:
        speak("Good Night sir!")
    speak("I am JARVIS, your personal assistant. How may I assist you?")



def take_command():
    """Capture voice input and convert to text."""
    r = sr.Recognizer()
    r.energy_threshold = 6000
    r.pause_threshold = 1
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in').lower()
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Could you please say that again?")
            return "none"
        except sr.RequestError as e:
            speak("Could not connect to the speech recognition service.")
            print(f"Error: {e}")
            return "none"
        except Exception as e:
            speak("An error occurred. Please try again.")
            print(f"Error: {e}")
            return "none"



def get_news_headline():

    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'ok' and data['articles']:
            headline = data['articles'][0]['title']
            return headline
        else:
            return "No news available at the moment."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return "Sorry, I couldn't fetch the news right now."



def jarvis():

    greet_user()
    while True:
        query = take_command()
        if query == "none":
            continue


        if 'exit' in query or 'stop' in query or 'bye' in query:
            hour = datetime.datetime.now().hour
            if 21 <= hour or hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
            break


        if 'open google' in query:
            speak(choice(opening_text))
            webbrowser.open("https://www.google.com")

        elif 'play love story' in query:
            speak(choice(opening_text))
            webbrowser.open("https://www.youtube.com/watch?v=WikAeXGsmHY&list=RDWikAeXGsmHY&start_radio=1")

        elif 'open grok' in query:
            speak(choice(opening_text))
            webbrowser.open("https://www.grok.com")
        

        elif 'open youtube' in query:
            speak(choice(opening_text))
            webbrowser.open("https://www.youtube.com")

        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif 'wikipedia' in query:
            speak(choice(opening_text))
            try:
                query = query.replace("wikipedia", "").strip()
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia...")
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Multiple results found. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find that page on Wikipedia.")
            except Exception as e:
                speak("An error occurred while searching Wikipedia.")
                print(f"Error: {e}")

        elif 'joke' in query:
            speak(choice(opening_text))
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'open notepad' in query and os.name == 'nt':
            speak(choice(opening_text))
            os.system("notepad.exe")

        elif 'news' in query or 'headline' in query:
            speak(choice(opening_text))
            headline = get_news_headline()
            speak("Here's the top headline...")
            speak(headline)

        else:
            speak("I'm not sure how to help with that. Please try another command.")


if __name__ == "__main__":
    jarvis()
