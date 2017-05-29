import lstm
import time
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import datetime, timedelta
from keras.models import model_from_json
import keras as keras
from random import randint
import os

from sklearn.externals import joblib

# cross-val
from keras.wrappers.scikit_learn import KerasClassifier
from keras import backend as backend
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

##
from os import path
import sys
sys.path.append(path.abspath('./data_preprocess'))
import data_preprocess.data as data

def predict(start_date, end_date,seq_len, model_path="../models/model.json"):
    '''
    Method used for predicting new data points

    input - start_date string in format of dd.mm.yyyy
            end_date string in format of dd.mm.yyyy
            seq_len - the length on which the model was trained
    
    returns predictions and the input_data
    '''

    # standard scaler JUST for y varaibles (otputs)
    standardScaler = joblib.load('../models/standardScaler.pkl')

    start_datetime = datetime.strptime(start_date, '%d.%m.%Y').date() - timedelta(days = seq_len)
    end_datetime = datetime.strptime(end_date, '%d.%m.%Y').date() + timedelta(days=1)
    
    data_input_pure = data.load_data_production(start_datetime, end_datetime)
    
    # standardise the data
    data_input = StandardScaler().fit_transform(data_input_pure.T).T
    data_input = lstm.divide_data_into_windows(data_input, seq_len)
    model = load_model(model_path)

    predictions = [lstm.predict_point_by_point(model, data_input)]
    predictions_destandardised = standardScaler.inverse_transform(predictions).tolist()

    # destroy session
    backend.clear_session()

    return predictions_destandardised, data_input_pure

def save_model(model, directory, file_name):
    '''
    Method saves the trained tensorflow model
    into a file for later evaluation
    '''

    if not os.path.exists(directory):
        os.makedirs(directory)

    model_name = directory+file_name

    # serialize model to JSON
    model_json = model.to_json()
    with open(model_name, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(directory+"/model.h5")
    print("Saved model to disk")

def load_model(model_path):
    '''
    Method saves a tensorflow model for evaluation
    '''
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model

    loaded_model.load_weights("../models/model.h5")
    print("Loaded model from disk")
    return loaded_model


if __name__=='__main__':
    '''
    Entry point of the application
    -- run this script to train a prediction model
    '''

    # number of epochs for training
    epochs  = 500

    # lenght of the training sequence
    seq_len = 2

    X_train, Y_train, X_test, Y_test, standardScaler = lstm.load_data('./DATA_INPUT.data', seq_len, True, True, train_test_mul=0.95)

    print("Bok")
    print(len(X_train) + len(X_test))

    base = "./Graph/"
    random_num = randint(0,99999999)
    full_path = base + str(random_num)

    tbCallBack = keras.callbacks.TensorBoard(log_dir=full_path, histogram_freq=0, write_graph=True, write_images=True)

    model = lstm.build_model([12, 50, 80, 1])
    model.fit(
    X_train,
    Y_train,
    batch_size=256,
    nb_epoch=epochs,
    validation_split=0.20
    , callbacks= [tbCallBack]
    )

    # save model
    save_model(model, "../models/"+str(random_num), "/model.json")

    print("Model saved!")
    print(random_num)
