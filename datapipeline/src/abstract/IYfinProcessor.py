from abc import ABC, abstractmethod

class IYFindProcessors(ABC):

    
    @abstractmethod
    def processData(self, dxy):
        pass
