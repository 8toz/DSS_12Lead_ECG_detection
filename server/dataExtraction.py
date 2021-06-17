import numpy as np
from scipy.io import loadmat
from filtering_methods import bandpass_filter, normalize, get_slices
import pandas as pd
import json
import os


csv_file = pd.read_csv("./data/Dx_snomed_valid.csv", delimiter=";")

lead_names = np.array(
    ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
)

filter_lowcut = 0.001
filter_highcut = 15.0
filter_order = 1


def get_features(file_name):

    
    print(file_name)
    # Cargamos los datos de los archivos y los inicializamos con NumPy
    data_dict = {}
    data = np.asarray(loadmat(file_name + ".mat")["val"], dtype=np.float64)

    # Abrimos el archivo .hea
    with open(file_name + ".hea", "r") as f:
        header_data = f.readlines()

    # De la primera linea extraemos la informacion relevante
    archivo, n_leads, fs, n_samples, _, _ = header_data[0].split()
    # Mapeamos el output de arriba con los valores relevantes de este
    n_leads, fs, n_samples = map(int, [n_leads, fs, n_samples])
    # Cada uno de estos los almacenamos en un diccionario
    data_dict["archivo"] = archivo
    data_dict["n_leads"] = n_leads
    data_dict["fs"] = fs
    data_dict["n_samples"] = n_samples
    data_dict["leads"] = []
    # por ejemplo data_dict --> {'n_leads': 12, 'fs': 500, 'n_samples': 7500, 'leads': []}

    # Iteramos a través del numero de derivaciones
    for i in range(n_leads):

        tmp = header_data[i + 1].split()

        # Nombre de la derivacion sobre la que se itera
        lead_name = tmp[-1].replace("\n", "")

        # Amplitude resolution
        gain_mv = int(tmp[2].lower().replace("/mv", ""))

        # Guardamos todos los valores en una nueva variable lead y la añadimos
        # a nuestro diccioanrio
        lead = {}
        lead["namestr"] = lead_name
        lead["name"] = np.where(lead_names == lead_name)[0]
        lead["gain_mv"] = gain_mv
        lead["samples"] = data[i]
        data_dict["leads"].append(lead)

    # A continuación se itera sobre todo el documendo .hea para extraer datos
    # sobre edad, sexo y la enfermedad
    for line in header_data:

        # Extraemos la edad
        if "#Age" in line:
            age = line.split(": ")[1]
            # Guardamos la edad y si esta no esta registrada le asignamos un valor arbitrario
            data_dict["age"] = int(age if not "NaN" in age else 57)
        # Extraemos el sexo si es (Masculino 0) si es (femenino 1)
        elif "#Sex" in line:
            data_dict["sex"] = (
                0 if line.split(": ")[1].replace("\n", "") == "Male" else 1
            )
        # IMPORTANTE
        # Extraemos la clase
        # Almacena el resultado de dicha clase en un array de N posiciones
        # que se corresponden con las N posibles clases del csv
        elif "#Dx" in line:
            data_dict["output"] = np.zeros((1, len(csv_file["Abbreviation"])))
            for c in line.split(": ")[1].replace("\n", "").split(","):
                for x in range(len(csv_file.index)):
                    if int(csv_file["SNOMED CT Code"][x]) == int(c):
                        data_dict["output"][0][x] = 1
        # Info de RX Hx y Sx en el .hea
        elif "#Rx" in line:
            data_dict["Rx"] = line.split(": ")[1].replace("\n", "")
        elif "#Hx" in line:
            data_dict["Hx"] = line.split(": ")[1].replace("\n", "")
        elif "#Sx" in line:
            data_dict["Sx"] = line.split(": ")[1].replace("\n", "")

    return data_dict


def isOutputEmpty(data_dict):
    '''
    Method that checks if the output does contains or not
    one of the 27 diseases. any() python method should also work
    '''

    if sum(data_dict["output"][0]) == 0:
        raise Exception("Check the list of available diseases")


def filterECG(data_dict):
    '''
    Filter method that returns the signals cleaned and filtered
    as four lists inputs, outputs, data_tags and ecg_leads
    '''

    n_samples = 0
    data_tags = []
    inputs = []
    outputs = []
    ecg_leads = []
    for lead in data_dict["leads"]:
        filtered = bandpass_filter(
            lead["samples"],
            lowcut=filter_lowcut,
            highcut=filter_highcut,
            signal_freq=data_dict["fs"],
            filter_order=filter_order,
        )
        for s in get_slices(filtered, freq=data_dict["fs"]):
            try:
                normalized = normalize(s)
            except:
                n_wrong += 1
                continue
            ecg_leads.append({"name": lead["namestr"], "signal": normalized.tolist()})
            data_tags.append(
                [
                    data_dict["archivo"],
                    data_dict["age"] if data_dict["age"] > 0 else 57,
                    data_dict["sex"],
                    data_dict["Rx"],
                    data_dict["Hx"],
                    lead["name"],
                ]
            )
            inputs.append(normalized)
            outputs.append(data_dict["output"][0])
            n_samples += 1

    print(n_samples)
    return inputs, outputs, data_tags, ecg_leads


def extract_dataframe(data_tags, inputs, outputs):
    '''
    Method that converts the info. returned from filterECG 
    into a pandas DataFrame
    '''
    # Dataframe de los data_tags
    df_tags = pd.DataFrame()
    df_tags = df_tags.append(data_tags)
    df_tags = df_tags.rename(
        columns={0: "file", 1: "age", 2: "sex", 3: "a", 4: "b", 5: "lead"}
    )
    df_tags = df_tags.drop(columns={"a", "b"})
    df_tags.head()

    # Dataframe de los inputs
    iniciador = {"ecg": []}
    df_inputs = pd.DataFrame(iniciador)
    total = []
    for input in inputs:
        total.append(input)

    clasificador = {"ecg": total}
    info = pd.DataFrame(clasificador)
    df_inputs = df_inputs.append(info, ignore_index=True)

    # Dataframe de los outputs
    iniciador = {"class": []}
    df_outputs = pd.DataFrame(iniciador)
    total = []
    for output in outputs:
        total.append(output.astype(int))

    clasificador = {"class": total}
    info = pd.DataFrame(clasificador)
    df_outputs = df_outputs.append(info, ignore_index=True)

    # Unimos los tres datasets en uno
    df_final = pd.DataFrame()
    df_final = pd.concat([df_tags, df_inputs, df_outputs], axis=1)
    df_final.head()

    return df_final


def remove_file_extension(file_name):
    '''
    Method that removes the file extension of the file .hea or mat
    and returns a file_name without the termination
    '''
    a = file_name.split("\\")
    file_name = a[-1].split(".")
    file_name = file_name[0]
    file_name = os.path.join("./uploads", file_name)

    return file_name


def extractData(file_name, format="json"):
    '''
    Returns the extracted data either in a json format
    to the front or a PandasDF to the NN
    '''
    data_dict = get_features(file_name)
    isOutputEmpty(data_dict)
    inputs, outputs, data_tags, leads = filterECG(data_dict)
    df = extract_dataframe(data_tags, inputs, outputs)
    result = df.to_json(orient="split")

    if format == "json":
        return result
    elif format == "dataframe":
        return df, leads
