import os
import subprocess as sp
import re
import imdb
from datetime import datetime
from random import choice
import keyboard
import pyttsx3
import wolframalpha
import speech_recognition as sr
from decouple import config
from conversation import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, news, weather_forcast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 185)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour <= 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you {USER}?")


listening = False


def start_listening():
    global listening
    listening = True
    print("Started Listening...")


def pause_listening():
    global listening
    listening = False
    print("Stopped Listening...")


keyboard.add_hotkey('ctrl+alt+l', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        user_query = r.recognize_google(audio, language='en-in')
        print(user_query)
        if not 'stop' in user_query or 'exit' in user_query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour <= 6:
                speak("good night sir, Take care!")
            else:
                speak("Have a good day sir!")
            exit()
    except Exception:
        speak("Sorry I could not understand. Can  you please repeat that?")
        user_query = 'None'
    return user_query


if __name__ == '__main__':
    greet()
    while True:
        if listening:
            query = listen_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you")
            elif "open command prompt" in query:
                speak("opening command prompt sir")
                os.system('start cmd')
            elif "open notepad" in query:
                speak("opening notepad for you sir")
                os.system('start notepad')
            elif "open camera" in query:
                speak("opening camera")
                sp.run('start microsoft.windows.camera:', shell=True)
            elif "open chrome" in query:
                speak("Opening google chrome.")
                # chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                # os.startfile(chrome_path)
                os.system('start chrome')
            elif "open vs code" in query:
                speak("Opening Visual Studio Code sir.")
                vs_code_path = "C:\\Users\\prath\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
                os.startfile(vs_code_path)
            elif "ip address" in query:
                my_ip_address = find_my_ip()
                speak(f"Your ip address is {my_ip_address}")
                print(f"Your ip address is {my_ip_address}")
            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = listen_command().lower()
                youtube(video)
            elif "open google" in query:
                speak(f"What do you want to search on google? {USER}")
                google_query = listen_command().lower()
                search_on_google(google_query)
            elif "open wikipedia" in query:
                speak("What do you want to search on wikipedia sir?")
                wikipedia_search = listen_command().lower()
                results = search_on_wikipedia(wikipedia_search)
                speak(f"According to wikipedia, {results}")
                speak("I am printing on terminal")
                print(results)
            elif "send an email" in query:
                speak("On what email address you want to send sir? Please enter in the terminal.")
                receiver_email = input("Email Address: ")
                speak("What should be the subject sir?")
                subject = listen_command().capitalize()
                speak("What is the message?")
                message = listen_command().capitalize()
                if send_email(receiver_email, subject, message):
                    speak("I have sent the email sir!")
                    print("I have sent the email sir!")
                else:
                    speak("Something went wrong! Please check the error log.")
            elif "give me news" in query:
                speak(f"I am reading the latest headlines of today, sir")
                speak(news())
                speak("I am printing it on the screen sir")
                print(*news(), sep='\n')
            elif "weather" in query:
                my_ip_address = find_my_ip()
                # city = requests.get(f"https://ipapi.co/{my_ip_address}/city").text
                speak("Please enter the name of your city sir")
                city = input("Enter the name of your city: ")
                speak(f"Getting weather report of your city {city}")
                weather, temp, feels_like = weather_forcast(city)
                speak(f"The temperature is {temp}, but feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("For your convenience, I am printing weather information on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels Like: {feels_like}")
            # elif "movie" in query:
            #     movies_db = imdb.IMDb()
            #     speak("Please tell me the movie name: ")
            #     text = listen_command()
            #     movies = movies_db.search_movie(text)
            #     if not movies:
            #         speak("Sorry sir, I couldn't find any movie with that name.")
            #     else:
            #         speak("Searching for " + text)
            #         speak("I found these:")
            #         movie = movies[0]
            #         title = movie.get("title", "Unknown Title")
            #         year = movie.get('year', 'Unknown Year')
            #         speak(f"{title} - {year}")
            #         info = movie.getID()
            #         movie_info = movies_db.get_movie(info)
            #         rating = movie_info.get("rating", "No rating available")
            #         cast = movie_info.get("cast", [])
            #         actor = cast[0:5] if cast else "No cast available"
            #         plot = movie_info.get('plot outline', 'Plot summary not available')
            #         speak(
            #             f"{title} was released in {year} and has an IMDb rating of {rating}. "
            #             f"It has actors like {actor}. "
            #             f"The plot summary is: {plot}."
            #         )
            #         print(
            #             f"{title} was released in {year} and has an IMDb rating of {rating}. "
            #             f"It has actors like {actor}. "
            #             f"The plot summary is: {plot}."
            #         )
            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name: ")
                text = listen_command()
                movies = movies_db.search_movie(text)
                if not movies:
                    speak("Sorry, I couldn't find any movie with that name.")
                else:
                    speak(f"Searching for {text}")
                    speak(f"I found these, please wait for some time to give you the details")
                    movie = movies[0]
                    movie_id = movie.getID()
                    movie_info = movies_db.get_movie(movie_id)
                    title = movie_info.get("title", "Unknown Title")
                    year = movie_info.get("year", "Unknown Year")
                    rating = movie_info.get("rating", "No rating available")
                    plot = movie_info.get('plot outline', 'Plot summary not available')
                    cast = movie_info.get("cast", [])
                    if cast:
                        actor_names = [person['name'] for person in cast[:5]]
                        actors_formatted = ", ".join(actor_names)
                    else:
                        actors_formatted = "No cast available"
                    speak(
                        f"{title} was released in {year} and has an IMDb rating of {rating}. "
                        f"It features actors like {actors_formatted}. "
                        f"The plot summary is: {plot}."
                    )
                    print(
                        f"{title} was released in {year} and has an IMDb rating of {rating}. "
                        f"It features actors like {actors_formatted}. The plot summary is: {plot}."
                    )
            elif "calculate" in query:
                app_id = "PUTK54-J5VLYTLP9Q"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    answer = next(result.results).text
                    match = re.search(r"[-+]?\d*\.\d+|\d+", answer)
                    if match:
                        number = float(match.group())
                        rounded_answer = round(number, 4)
                        speak(f"The answer is approximately {rounded_answer}")
                        print(f"The answer is approximately {rounded_answer}")
                    else:
                        speak("The answer is " + answer)
                        print("The answer is " + answer)
                except StopIteration:
                    speak("I could not find that. Please try again")
            elif "what is" in query or "who is" in query or "which is" in query:
                app_id = "PUTK54-J5VLYTLP9Q"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                            query.lower().index('which is') if 'which is' in query.lower() else None
                    if ind is not None:
                        text = query.split()[ind + 2:]
                        result = client.query(" ".join(text))
                        answer = next(result.results).text
                        speak("The answer is " + answer)
                        print("The answer is " + answer)
                    else:
                        speak("I could not find that")
                except StopIteration:
                    speak("I could not find that. Please try again.")
