
from abc import ABC, abstractmethod

import pandas as pd
class IDataVisualizerController(ABC):


    @abstractmethod
    def loadCsv() -> pd.DataFrame:
        pass


    @abstractmethod
    def visualizeData():
        pass
    