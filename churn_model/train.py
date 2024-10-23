import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
import pickle


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

C = 1.0
n_splits = 5
MODEL_FILE = "model.bin"


def train(df_train, y_train, C=1.0):
    dv = DictVectorizer(sparse=False)
    dicts = df_train[categorical + numerical].to_dict(orient="records")
    X_train = dv.fit_transform(dicts)
    model = LogisticRegression(C=C, max_iter=1000)
    model.fit(X_train, y_train)
    return dv, model

def predict(df, dv, model):
    """Predict the probability of churn."""
    dicts = df[categorical + numerical].to_dict(orient="records")
    X = dv.transform(dicts)
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred


if __name__ == "__main__":
    df = pd.read_csv("churn.csv")
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    categorical_columns = df.select_dtypes(include=["object"]).columns
    for col in categorical_columns:
        df[col] = df[col].str.lower().str.replace(" ", "_")
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce")
    df.totalcharges = df.totalcharges.fillna(0)
    df.churn = (df.churn == "yes").astype(int)
    df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
    df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)
    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)
    y_train = df_train.churn.values
    y_val = df_val.churn.values
    y_test = df_test.churn.values
    del df_train["churn"]
    del df_val["churn"]
    del df_test["churn"]
    
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)
    scores = []

    for train_idx, val_idx in kfold.split(df_full_train):
        df_train = df_full_train.iloc[train_idx]
        df_val = df_full_train.iloc[val_idx]

        y_train = df_train.churn.values
        y_val = df_val.churn.values

        dv, model = train(df_train, y_train, C=C)
        y_pred = predict(df_val, dv, model)

        score = roc_auc_score(y_val, y_pred)
        scores.append(score)

    print("C=%s %.3f +- %.3f" % (C, np.mean(scores), np.std(scores)))

    with open(MODEL_FILE, "wb") as f_out:
        pickle.dump((dv, model), f_out)
