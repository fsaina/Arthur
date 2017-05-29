from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin

import numpy as np
import datetime

from os import path
import sys
sys.path.append(path.abspath('./data_preprocess/'))

import chiller_reading_data as chiller_readings
import weather_data

def __get_additional_data__(dates):
    '''
    Method used for creating additional data
    as features for input
    '''
    day_of_week = list(map(lambda date: date[0].weekday(), dates))
    return np.reshape(np.array(day_of_week), (len(day_of_week), 1))


def create_datetime_date_list(start_date,end_date):
    one_day_offset = datetime.timedelta(days = 1)
    diff = end_date - start_date + one_day_offset

    dates = list()
    for i in range(diff.days):
        date = start_date + datetime.timedelta(days = i)
        dates.append([date])
    return np.array(dates)

def load_data_production(start_date, end_date):
    '''
    start_date - datetime.date
    end_date   - datetime.date
    '''
    wd = weather_data.get_weather_data_for_time_interval(start_date, end_date, force=True)
    dates = create_datetime_date_list(start_date, end_date)
    data_additional = __get_additional_data__(dates)

    return np.concatenate( [wd, data_additional], axis=1 )

def load_data():
    '''
    data.py -- main preprocess data function. Call this one when
    input is needed
    '''
    # chiller_data
    cd = chiller_readings.load_time_reading_pair_data()

    start_date = cd[0][0]
    end_date = cd[len(cd)-1][0]

    # weather data
    wd = weather_data.get_weather_data_for_time_interval(start_date, end_date)

    # concatinate the data into: y x1 x2 x3 ... xn
    data = np.concatenate( (cd[:,1:2], wd), axis=1 )

    # postdata inclusion
    data_additional = __get_additional_data__(cd[:,0:1])

    # concatendate the additional data on the end!
    data = np.concatenate( (data, data_additional), axis=1)

    # np array of: y x1 x2 ... xn
    return data
