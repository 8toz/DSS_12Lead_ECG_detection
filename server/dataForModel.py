import numpy as np
from keras.utils import np_utils
from tensorflow.keras.models import load_model
from dataExtraction import extractData
import os
import json


def transform_data(dataset):
    '''
    Prepares the data to feed the Neural Network by transforming the shape 
    from the dataset
    '''

    if dataset.keys()[0] == "ecg":
        aux = dataset["ecg"].values
        newX = []
        [newX.append(ecg) for ecg in aux]
        newX = np.asarray(newX)
        print(f"ECG transformados con exito! dimensiones -> {newX.shape}")
        return newX

    elif dataset.keys()[0] == "age":
        age = (dataset["age"].values.astype(int)).reshape((len(dataset["age"]), -1))
        sex = (dataset["sex"].values.astype(int)).reshape((len(dataset["sex"]), -1))
        lead = (dataset["lead"].values.astype(int)).reshape((len(dataset["lead"]), -1))

        qual = np.concatenate((age, sex, lead), axis=-1)
        print(
            f"Datos cualitativos transformados con exito! dimensiones -> {qual.shape}"
        )
        return qual

    elif dataset.keys()[0] == "class":
        aux = dataset["class"].values
        newy = []
        [newy.append(label) for label in aux]
        newy = np.asarray(newy)
        print(f"Clases transformadas con exito! dimensiones -> {newy.shape}")
        return newy


def dataForPrediction(dataset):
    '''
    Method that uses the transform method from above to match the NN desired input
    '''
    X, qual = dataset[["ecg"]], dataset[["age", "sex", "lead"]]
    X = transform_data(X)
    qual = transform_data(qual)

    return X, qual


def compute_predictions(df, model):
    '''
    Method in charge of computing the predictions from the Neural Network
    returning a score and the label tag associated
    '''

    X, qual = dataForPrediction(df)
    y = model.predict([X, qual])

    for i in range(y.shape[0]):
        argsmax = np.argsort(-y[i])
        argmax = y[i][argsmax[0]]
        y[i] = (y[i] == argmax) + np.zeros((27,))

    current_score = np.sum(y, axis=0) / y.shape[0]
    current_label = (current_score > 0.6) + np.zeros((27,))

    # if(np.sum(current_label) == 0):
    #    agmax = current_score[np.argmax(current_score)]
    #    current_label = ((current_score == agmax) + np.zeros((27,)))

    # if math.isnan(current_label[0]):
    #     current_label = np.zeros((27,))

    return current_label, current_score
