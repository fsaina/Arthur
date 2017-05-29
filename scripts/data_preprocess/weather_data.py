import requests
import datetime

from pathlib import Path

from sklearn.pipeline import Pipeline
import numpy as np

URL = "https://api.darksky.net/forecast/c4ad5c64e3300872e5128d32d764ad0e/45.8150,15.9819,"

def __grab_weather_for_unix_time__(unix_time):
    """
    Consider that this functions returns the wather info 
    for the day BEFORE the given unix_time value
    """
    url = URL + str(unix_time)

    r = requests.get(url = url)
    json_response = r.json()

    data =json_response['daily']['data'][0]

    moonPhase = data['moonPhase']
    temp_min = data['temperatureMin']
    temp_max = data['temperatureMax']
    apperent_temp_min = data['apparentTemperatureMin']
    apperent_temp_max = data['apparentTemperatureMax']
    dewPoint = data['dewPoint']
    humidity = data['humidity']
    windSpeed = data['windSpeed']
    windBearing = data['windBearing']
    cloudCover = data['cloudCover']
    pressure = data['pressure']

    current_day = [
              str(moonPhase)
            , str(temp_min)
            , str(temp_max)
            , str(apperent_temp_min)
            , str(apperent_temp_max)
            , str(dewPoint)
            , str(humidity)
            , str(windSpeed)
            , str(windBearing)
            , str(cloudCover)
            , str(pressure)
            ]
    return current_day

def get_weather_data_for_time_interval(start_date, end_date, force = False):
    '''
    Method returns a numpy array of read weather values.

    Input: two datetime.date objects defining start and end dates
    Weather info is returned on daily basis
    '''
    one_day_offset = datetime.timedelta(days = 1)
    # api returns the complete summary from the day before (so we need to ask for one day latter that intended)

    # INITIAL_DATE = datetime.datetime.strptime('01.04.2017', "%d.%m.%Y") + one_day_offset
    # END_DATE = datetime.datetime.strptime('04.05.2017', "%d.%m.%Y") + one_day_offset


    weather_data_file = Path("./data_preprocess/weather.data")
    if weather_data_file.is_file() and force == False:
        #read data from file instead online

        with open("./data_preprocess/weather.data", "r") as w_file:
            return np.loadtxt(w_file)

    diff = end_date - start_date + one_day_offset

    data_list = list()
    for i in range(diff.days):
        #offset
        datetime_days = datetime.timedelta(days = i)
        time = start_date + one_day_offset + datetime_days
        unix_time = int(time.strftime("%s"))
        data_list.append(__grab_weather_for_unix_time__(unix_time))

        print("Getting weather data for day: ", str(time))


    data = np.array(data_list)
    # write weather data to file
    #np.savetxt("./data_preprocess/weather_temp.data", data)

    return data
