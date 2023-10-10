import time

import requests
from datetime import datetime
import smtplib

MY_EMAIL = "onehundreddaysofcode86@gmail.com"
PASSWORD = "mfyyedxmejkjecuy"

MY_LAT = 41.436080
MY_LONG = -8.284860


def is_iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = time_now.hour
    if hour <= sunrise or hour >= sunset:
        return True


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="jopantaleao@gmail.com", msg="Subject:Look Up\n\n"
                                                                                      "ISS Station is passing by.")


while True:
    iss_result = is_iss_near()
    hour_result = is_dark()

    if iss_result and hour_result:
        send_email()
    time.sleep(60)

# #If the ISS is close to my current position
# # and it is currently dark
# # Then send me an email to tell me to look up.
# # BONUS: run the code every 60 seconds.
