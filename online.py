import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL=config('EMAIL')
PASSWORD=config('PASSWORD')

def find_my_ip():
    my_ip_address=requests.get('https://api.ipify.org?format=json').json()
    return my_ip_address["ip"]

def search_on_wikipedia(query):
    results=wikipedia.summary(query,sentences=2)
    return results

def search_on_google(user_query_for_google_search):
    kit.search(user_query_for_google_search)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_email,subject,message):
    try:
        email=EmailMessage()
        email['To']=receiver_email
        email['Subject']=subject
        email['From']={EMAIL}

        email.set_content(message)
        s=smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False

def news():
    news_headlines=[]
    news_result=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey"
                             f"=8394ad7eceb74ec795f8ce3e2698628a").json()
    articles=news_result["articles"]
    for articles in articles:
        news_headlines.append(articles["title"])
    return news_headlines[:6]

def weather_forcast(city):
    res=requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=7f049881e36fe1c9274a00c26ef10cfc"
    ).json()
    weather=res["weather"][0]["main"]
    temp=res["main"]["temp"]
    feels_like=res["main"]["feels_like"]
    return weather,f"{temp} degree Celcius",f"{feels_like} degree Celcius"