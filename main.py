import requests
import datetime as dt
import smtplib
import time


LAT = 51.507351
LNG = -0.127758
MY_EMAIL = 'jaltura1997@gmail.com'
PASSWORD = 'gnphcazrmfzwahhx'


def iss_pos():
    """
    Returns true if ISS position is close to our position otherwise false.
    :return:
    """
    iss_response = requests.get(url='http://api.open-notify.org/iss-now.json')
    iss_response.raise_for_status()

    data = iss_response.json()
    iss_lat = float(data['iss_position']['latitude'])
    iss_lng = float(data['iss_position']['longitude'])

    # distance_lat = LAT - iss_lat
    # distance_lng = LNG - iss_lng
    # if -5 < distance_lng < 5 and -5 < distance_lng < 5: can also be used to
    # determine distance from ISS

    if LAT-5 < iss_lat < LAT+5 and LNG-5 < iss_lng < LNG+5:
        return True


def nighttime():
    """
    Returns true if current time is nighttime otherwise false
    :return:
    """
    parameters = {
        'lat': LAT,
        'lng': LNG,
        'formatted': 0
    }

    response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters, )
    response.raise_for_status()

    data = response.json()
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']

    sunrise_hour = int(sunrise.split('T')[1].split(':')[0])
    sunset_hour = int(sunset.split('T')[1].split(':')[0])

    today = dt.datetime.now()
    today_hour = today.hour

    if sunset_hour <= today_hour <= sunrise_hour:
        return True


while True:
    time.sleep(60)
    if iss_pos() and nighttime():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs='testingpython17463@yahoo.com',
                                msg='Subject:ISS ALERT!\n\nISS is near you and its evening right now so there is a '
                                    'good chance that you can get a glance so LOOK UP!'
                                )
