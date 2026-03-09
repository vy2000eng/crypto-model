from abc import ABC, abstractmethod

class IYFindClient(ABC):

    
    @abstractmethod
    def fetch_dxy_data(self):
        pass
