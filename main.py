import requests
from datetime import datetime
import smtplib
from constants import *
from time import sleep

def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    if (MY_LAT - 5) < iss_lat < (MY_LAT + 5) and (MY_LNG - 5) < iss_lng < (MY_LNG + 5):
        return True
    

def is_night():
    params = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("http://api.sunrise-sunset.org/json", params=params)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now > sunset or time_now < sunrise:
        return True

while True:
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP(HOST)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PWD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up☝️\n\nISS is above!"
        )
    sleep(60)