from abc import ABC, abstractmethod
import pandas as pd
from xgboost import XGBClassifier



class IModelController(ABC):
    pass

    @abstractmethod
    def getFeatures(self) -> list:
        pass

    @abstractmethod
    def getDf(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def definelabe(self,df:pd.DataFrame) -> pd.DataFrame:
        pass
    @abstractmethod
    def getHyperParams(self) -> dict:
        pass

    @abstractmethod
    def define_model(self,hyper_params:dict) -> XGBClassifier:
        pass

    @abstractmethod
    def def_test_train_data(X:pd.DataFrame,y:pd.DataFrame,split:int)->tuple:
        pass
    @abstractmethod
    def save_model(self,model:XGBClassifier,FEATURES:list) -> None:
        pass






