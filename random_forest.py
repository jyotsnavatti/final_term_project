# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xsf_W0PMXjrR9W_yMsJ8H6PZb0aUJyTU
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_auc_score

def calculate_metrics(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    tss = (tp / (tp + fn)) - (fp / (fp + tn))
    hss = 2 * (tp * tn - fp * fn) / ((tp + fn) * (fn + tn) + (tp + fp) * (fp + tn))
    return {"TP": tp, "TN": tn, "FP": fp, "FN": fn, "FPR": fpr, "FNR": fnr, "TSS": tss, "HSS": hss}

def random_forest_model(X, y):
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    metrics_list = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)

        metrics = calculate_metrics(y_test, y_pred)
        metrics["ROC_AUC"] = roc_auc_score(y_test, rf_model.predict_proba(X_test)[:, 1])
        metrics_list.append(metrics)

    return pd.DataFrame(metrics_list)