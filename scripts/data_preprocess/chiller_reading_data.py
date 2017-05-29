import csv
from datetime import datetime

from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin

from collections import defaultdict

import numpy as np

import statistics as s

class PhazeTransform(TransformerMixin):

    def transform(self, readings):
        # remove header
        del readings[0]

        readings_new = list()
        for i in range(len(readings)):
            first = (readings[i][0], readings[i][1])
            second = (readings[i][2], readings[i][3])
            readings_new.append(first)
            readings_new.append(second)

        return readings_new

    def fit(self, *_):
        return self

class DayFoldTransform(TransformerMixin):

    def transform(self, readings):
        '''
        input: list of tuples -> (date_time, reading)
        '''

        date_value_map = defaultdict(list)
        for (date_time, value) in readings:

            if date_time == '':
                continue

            date_format = "%d.%m.%Y"
            date_str = date_time.split(' ')[0]
            date_object = datetime.strptime(date_str, date_format).date()
            
            date_value_map[date_object].append(value)

        date_list = list()
        for key in date_value_map.keys():
            value_list = date_value_map[key]
            #convert from string to float
            value_list = list(map( lambda e: float(e.replace(",", ".")), value_list))
            mean_value = s.mean(value_list)
            #mean_value = max(value_list)
            power_value = mean_value
            pair = (key, power_value)
            date_list.append(pair)

        date_list.sort(key= lambda p: p[0])
        return np.array(date_list)

    def fit(self, *_):
        return self

def __load_data__(file_path):
    data = list()

    with open(file_path, encoding='utf-16-le') as f:
        reader = csv.reader(f, delimiter =";")
        for row in reader:
            data.append(row)

    return data

###
# MAIN
###

def load_time_reading_pair_data():

    pipeline = Pipeline([
                ("merge phases", PhazeTransform())
        ,       ("fold_times_into_days", DayFoldTransform())
        ])

    transformed_data_ru1 = np.array(pipeline.transform(__load_data__(file_path="./data_170503/OnlineTrendControl/RU211_15.csv")))
    transformed_data_ru2 = np.array(pipeline.transform(__load_data__(file_path="./data_170503/OnlineTrendControl/RU212_15.csv")))
    transformed_data_start_gro = np.array(pipeline.transform(__load_data__(file_path="./data_170503/OnlineTrendControl/STARI_GRO_15.csv")))

    dates_vector = transformed_data_ru1[:,0:1]


    value_sum = transformed_data_ru1[:,1:2] + transformed_data_ru2[:, 1:2] + transformed_data_start_gro[:,1:2]

    return np.concatenate( (dates_vector, value_sum), axis=1 )
