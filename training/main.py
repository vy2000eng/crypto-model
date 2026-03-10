
#from datapipeline.src.utils.EnvVars import EnvVars#..datapipeline.src.utils.EnvVars import EnvVars
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import joblib
import pandas as pd
import joblib
import os
from src.utils.EnvVars import EnvVars
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import numpy as np
from  src.controller.ModelController import ModelController


if __name__ == "__main__":
    modelController = ModelController()
    df              = modelController.getDf()
    FEATURES        = modelController.getFeatures()
    df              = modelController.definelabe(df)
    X               = df[FEATURES]
    y               = df["target"]
    split           = int(len(df) * 0.8)
    X_train,X_test,y_train,y_test = modelController.def_test_train_data(X,y,split)
    hyper_params                  = modelController.getHyperParams()
    model                         = modelController.define_model(hyper_params)
    model.fit                       (X_train, y_train)
    modelController.evaluate_model  (model,y_test,X_test)
    modelController.save_model      (model,FEATURES)

