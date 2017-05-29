import os
import warnings
import time
import numpy as np
from numpy import newaxis
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer


from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras import optimizers

from sklearn.externals import joblib

import data_preprocess.data as input_data

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Hide messy TensorFlow warnings
warnings.filterwarnings("ignore") #Hide messy Numpy warnings


def divide_data_into_windows(data, seq_len):
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])
    result = np.array(result)
    return result


def load_data(filename, seq_len, normalise_window, standardise_data, train_test_mul=0.9):
    data = input_data.load_data()
    number_of_features = 12

    data,ss_y = standardise_data_fun(data)

    result = divide_data_into_windows(data, seq_len)

    row = round(train_test_mul * result.shape[0])
    train = result[:int(row), :]

    x_train = train[:, :-1, 1:]
    y_train = train[:, -1, 0]

    x_test = result[int(row):, :-1, 1:]
    y_test = result[int(row):, -1, 0]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], number_of_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], number_of_features))  

    return [x_train, y_train, x_test, y_test, ss_y]

def standardise_data_fun(data, ss_y=StandardScaler()):
    data_y = data[:,0:1]
    y_standardised = ss_y.fit_transform(data_y)
    data_standardised = StandardScaler().fit_transform(data.T).T
    # TODO logaritmiraj input podatke !!! -> bolje performanse

    # save the standardScaler object to file as it will
    # be used for prediction
    joblib.dump(ss_y, '../models/standardScaler.pkl') 

    data = np.concatenate( (y_standardised, data_standardised[:, 1:]), axis =1 )

    return data, ss_y

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [ np.concatenate( ([((float(p[0]) / float(window[0][0])) - 1)],p[1:])) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data

def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        activation="softsign",
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        activation="softsign",
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation("linear"))


    #change just the lr parameter !!!
    rms_prop = optimizers.RMSprop(lr=0.000154, rho=0.9, epsilon=1e-08, decay=0.0)

    model.compile(loss="mse", optimizer=rms_prop)
    return model

def predict_point_by_point(model, data):
    #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted.tolist()

def predict_sequence_full(model, data, window_size):
    #Shift the window by 1 new prediction each time, re-run predictions on new window
    curr_frame = data[0]
    predicted = []
    for i in range(len(data)):
        predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
        curr_frame = curr_frame[1:]
        curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
    return predicted

def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of 50 steps before shifting prediction run forward by 50 steps
    prediction_seqs = []
    for i in range(int(len(data)/prediction_len)):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs
