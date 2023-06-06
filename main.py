import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv({"C:/YOUR_LOCATION/"})

OPENWEATHER_API_KEY = os.getenv("OpenWeather_API_Key")
account_sid = os.getenv("Twilio_Account_SID")
auth_token = os.getenv("Twilio_Auth_Token")
MY_LAT = 44.5542769
MY_LONG = -64.3437215

params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily,alerts",
    "appid": OPENWEATHER_API_KEY
}

response = requests.get("https://api.openweathermap.org/data/3.0/onecall", params=params)
response.raise_for_status()

weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔",
        from_={"FROM_PHONE_NUMBER"},
        to={"TO_PHONE_NUMBER"}
    )
    print(message.status)

