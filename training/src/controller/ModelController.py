
from src.abstract.IModelController import IModelController
from src.utils.EnvVars import EnvVars
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import os
import joblib
from sklearn.metrics import roc_auc_score




class ModelController(IModelController):
    def __init__(self):
        self.envVars = EnvVars()

    def getFeatures(self) -> list:
        return list(self.envVars.FEAUTURES.split(","))
    
    def getDf(self) -> pd.DataFrame:
        return pd.read_csv(self.envVars.TRAINING_DATA_PATH_MARK_STRUCT)
    
    def definelabe(self,df:pd.DataFrame) -> pd.DataFrame:
        df["future_volatility"] = df["future_return_6h"].abs()
        threshold = df["future_volatility"].quantile(0.75)
        df["target"] = (df["future_volatility"] > threshold).astype(int)
        print(df["target"].value_counts(normalize=True))
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna()
        return df
    
    def getHyperParams(self) -> dict:
        return {
                "n_estimators":self.envVars.N_ESTIM,
                "max_depth":self.envVars.MAX_DEPTH,
                "learning_rate":self.envVars.LEARNING_RATE,
                "subsample":self.envVars.SUBSMPLE,
                "colsample_bytree":self.envVars.COLSMPL_BY_TREE,
                "random_state":self.envVars.RANDOM_ST,
                }
    
    def define_model(self,hyper_params) -> XGBClassifier:
            return XGBClassifier(
                n_estimators     =int(hyper_params["n_estimators"]),
                max_depth        =int(hyper_params["max_depth"]),
                learning_rate    =int(hyper_params["learning_rate"]),
                subsample        =int(hyper_params["subsample"]),
                colsample_bytree =int(hyper_params["colsample_bytree"]),
                random_state     =int(hyper_params["random_state"])
            )
    def def_test_train_data(X:pd.DataFrame,y:pd.DataFrame,split:int)->tuple:
         return split,X.iloc[:split],X.iloc[split:],y.iloc[:split],y.iloc[split:]
         
    def save_model(self,model,FEATURES):
         
        os.makedirs("models", exist_ok=True)

        joblib.dump(model, self.envVars.MODEL_OUTPUT)
        joblib.dump(FEATURES, self.envVars.FEATURES_OUTPUT)
        print("model saved")

    def evaluate_model(model:XGBClassifier,y_test:pd.DataFrame,X_test:pd.DataFrame):
        proba = model.predict_proba(X_test)[:,1]

        auc = roc_auc_score(y_test, proba)

        print("AUC:", auc)
        
         
            
        

         



    

        

