import pickle
from flask import Flask, request


MODEL_FILE = "model.bin"

numerical = ["tenure", "monthlycharges", "totalcharges"]

categorical = [
    "gender",
    "seniorcitizen",
    "partner",
    "dependents",
    "phoneservice",
    "multiplelines",
    "internetservice",
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
    "streamingtv",
    "streamingmovies",
    "contract",
    "paperlessbilling",
    "paymentmethod",
]

app = Flask("churn")

@app.route("/predict", methods=["POST"])
def predict_churn():
    customer = request.json
    with open(MODEL_FILE, "rb") as f_in:
        dv, model = pickle.load(f_in)
        X = dv.transform([customer])
        pred = model.predict_proba(X)[0, 1]
        return {"churn_probability": pred}


if __name__ == "__main__":

    with open(MODEL_FILE, "rb") as f_in:
        dv, model = pickle.load(f_in)

    customer = {
        'gender': 'female',
        'seniorcitizen': 0,
        'partner': 'yes',
        'dependents': 'no',
        'phoneservice': 'no',
        'multiplelines': 'no_phone_service',
        'internetservice': 'dsl',
        'onlinesecurity': 'no',
        'onlinebackup': 'yes',
        'deviceprotection': 'no',
        'techsupport': 'no',
        'streamingtv': 'no',
        'streamingmovies': 'no',
        'contract': 'month-to-month',
        'paperlessbilling': 'yes',
        'paymentmethod': 'electronic_check',
        'tenure': 1,
        'monthlycharges': 29.85,
        'totalcharges': 29.85
    }

    tr = dv.transform([customer])
    pred = model.predict_proba(tr)[0, 1]
    print(f"Churn probability: {pred}")