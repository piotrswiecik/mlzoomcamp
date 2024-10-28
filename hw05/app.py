import pickle
from flask import Flask, request, jsonify

MODEL_FILE = "model1.bin"
DV_FILE = "dv.bin"

app = Flask("model")


def load():
    with open(MODEL_FILE, "rb") as f_in:
        model = pickle.load(f_in)
    with open(DV_FILE, "rb") as f_in:
        dv = pickle.load(f_in)
    return dv, model


@app.route("/model", methods=["POST"])
def predict():
    try:
        data = request.json
    except AttributeError:
        return jsonify({"error": "Invalid data"})
    dv, model = load()
    X = dv.transform([data])
    pred = model.predict_proba(X)[0, 1]
    return jsonify({"probability": pred})
