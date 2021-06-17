from flask import Flask, render_template, jsonify, request, session, redirect, flash, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from parent_class import ClassifierInterface
import json
import os
import logging

app = Flask(__name__)

MAX_CONTENT_LENGTH = 1024 * 1024
ALLOWED_EXTENSIONS = ["hea", "mat"]
UPLOAD_FOLDER = "./uploads"
app.secret_key = "super secret key"


classifier = ClassifierInterface()


def allowed_combination(filename1, filename2):
    if filename2.split(".")[0] == filename1.split(".")[0]:
        if (".hea" in filename1 and ".mat" in filename2) or (
            ".hea" in filename2 and ".mat" in filename1
        ):
            return allowed_file(filename2) and allowed_file(filename1)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadData", methods=["POST", "GET"])
@cross_origin()
def storeFiles():
    print(request.files)
    if "file1" not in request.files or "file2" not in request.files:
        flash("No file part")
        return redirect(request.url)
    f1 = request.files["file1"]
    f2 = request.files["file2"]

    if f1.filename == "" or f2.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if f1 and f2 and allowed_combination(f1.filename, f2.filename):
        # filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(f1.filename))
        filepath1 = os.path.join(UPLOAD_FOLDER, f1.filename)
        # filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(f2.filename))
        filepath2 = os.path.join(UPLOAD_FOLDER, f2.filename)
        print("Guardamos el primer archivo")
        f1.save(filepath1)
        print("Guardamos el segundo archivo")
        f2.save(filepath2)

        if ".mat" in filepath1:
            current_label, current_score, leads, classes, fs = classifier.gatherinfo(
                filepath1
            )
        else:
            current_label, current_score, leads, classes, fs = classifier.gatherinfo(
                filepath2
            )
        os.remove(filepath2)
        os.remove(filepath1)

        response = {}
        response["leads"] = leads
        response["classes"] = classes.tolist()
        response["labels"] = current_label.tolist()
        response["score"] = current_score.tolist()
        response["fs"] = fs
        

    return response

@app.route("/sendImage", methods=["GET"])
@cross_origin()
def download_printable():
    route = './preprint_ECG/ECG_for_NN.png'
    return send_file(route)

@app.route("/getFeatures", methods=["GET"])
@cross_origin()
def download_json():
    route2 = "./ecg_features_json/result.json"
    return send_file(route2)


if __name__ == "__main__":
    app.run(debug=True)
