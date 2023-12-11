import time
import requests
import datetime as dt
import smtplib

MY_LAT = 42.360081
MY_LONG = -71.058884
MY_EMAIL = "bigdrd@gmail.com"
MY_PASSWORD = "as8d78s9d7as89"


def is_iss_overhead():
    response1 = requests.get(url="http://api.open-notify.org/iss-now.json")

    data = response1.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data2 = response.json()
    sunrise = data2["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data2["results"]["sunset"].split("T")[1].split(":")[0]

    time_now = dt.datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up\n\nThe ISS is above you in the sky."
        )
