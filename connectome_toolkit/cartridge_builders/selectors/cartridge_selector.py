from abc import ABC, abstractmethod

class CartridgeSelector(ABC):
    @abstractmethod
    def select(self, builder : "CartridgeBuilder"):
        pass
