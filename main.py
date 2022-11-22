import requests
import datetime as dt
import smtplib

MY_EMAIL = ""
MY_PASS = ""

loc_parameters = {
    "lat": 40.712776,
    "lng": -74.005974,
    "formatted": 0
}

sunrise_sunset = requests.get("https://api.sunrise-sunset.org/json", params=loc_parameters)
sunrise_sunset.raise_for_status()
sunrise_sunset_json = sunrise_sunset.json()

iss_loc = requests.get("http://api.open-notify.org/iss-now.json")
iss_loc.raise_for_status()
iss_loc_json = iss_loc.json()

sunset_hour = int(sunrise_sunset_json["results"]["sunset"].split("T")[1].split(":")[0]) + 1
sunrise_hour = int(sunrise_sunset_json["results"]["sunrise"].split("T")[1].split(":")[0]) - 1

time_now_hour = dt.datetime.now().hour

if time_now_hour >= sunset_hour or time_now_hour <= sunrise_hour:
    location_lat_long_iss = (float(iss_loc_json["position"]["lattitude"]), float(iss_loc_json["position"]["longtitude"]))
    rounded_lat_long_pos = (round(loc_parameters["lat"], 2), round(loc_parameters["lng"], 2))
    if rounded_lat_long_pos[0] <= location_lat_long_iss[0] <= rounded_lat_long_pos[0] + 1 and rounded_lat_long_pos[1] <= location_lat_long_iss[1] <= rounded_lat_long_pos[1] + 1:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASS)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: Look up!\n\nISS is over head!")