from django.shortcuts import render
from django.http import JsonResponse
import time

###
# prediction py
###
from datetime import datetime
from datetime import timedelta

from os import path
import sys
sys.path.append(path.abspath('../scripts/'))
sys.path.append(path.abspath('../scripts/data_preprocess/'))
import run

# Create your views here.
def dashboard_page(request):
    prediction_label = "Skladište 1"

    return render(request, 'dashboard/index.html', {
         "prediction_label" : prediction_label
        })

# graph request to return data
def predict_data(request):
    if request.GET['dana'] :
        prediction_days = int(request.GET['dana'])
        
        # the length of the sequence with which the tensorflow model was trained
        seq_len = 2


        current = datetime.now()
        diff = timedelta(days=prediction_days)

        # set inital dates
        initial_date_str = current.strftime("%d.%m.%Y")
        end_date_str = (current+diff).strftime("%d.%m.%Y")

        # predict series
        data_predictions, data_input = run.predict(initial_date_str, end_date_str, seq_len)

        # generate date labels
        labels = list()
        for d in range(prediction_days+1):
            diff = timedelta(days=d)
            date = current + diff
            date_str = date.strftime("%d.%m.%Y")
            labels.append(date_str)

        # calculate kW into kWh
        predictions = data_predictions[0]
        # round predictions
        predictions = list(map( lambda prediction: round(prediction, 3)  ,predictions))
        prediction_energy_sum = round(sum(predictions) * 24, 2)

        # extract max temperature values from input data and convert farenheit to celsius
        max_temperatures = list(map( lambda farenheit: round((float(farenheit[0]) - 32) * 5/9, 2) , data_input[:, 2:3].tolist() ))

        # remove last 3 element-s if seq len = 2
        max_temperatures = max_temperatures[:(-seq_len - 1)]

        json = {
                'prediction_list' : predictions
            , "prediction_labels" : labels
            , "prediction_energy_sum" : prediction_energy_sum
            , "prediction_days" : prediction_days
            , "maximum_temperatures_list" : max_temperatures
                }
        return JsonResponse(json)

    else:
        return ">dana< parameter not set!"

