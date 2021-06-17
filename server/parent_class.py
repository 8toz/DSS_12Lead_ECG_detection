import numpy as np
import tensorflow as tf
import pandas as pd
import json
from tensorflow.keras.models import load_model
from dataExtraction import extractData, get_features, remove_file_extension
from dataForModel import compute_predictions
from ecg_printable_plot import upload_image_print
from ecg_features import get_ECG_features

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ClassifierInterface(metaclass=Singleton):
    def __init__(self):

        self.model = load_model("./dnn/model1.h5")
        self.CSV_FILE = pd.read_csv("./data/Dx_snomed_valid.csv", delimiter=";")
        self.classes = np.array(self.CSV_FILE["Abbreviation"])

    def gatherinfo(self, file_path):
        file_path = remove_file_extension(file_path)
        data_dict = get_features(file_path)
        upload_image_print(data_dict)
        ecg_features = get_ECG_features(data_dict)
        with open('./ecg_features_json/result.json', 'w') as fp:
            json.dump(ecg_features, fp)
        df, leads = extractData(file_path, format="dataframe")
        current_label, current_score = compute_predictions(df, self.model)
        fs = data_dict["fs"]

        return current_label, current_score, leads, self.classes, fs
