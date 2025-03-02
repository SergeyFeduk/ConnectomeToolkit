from abc import ABC, abstractmethod
from src.cartridge_builders.cartridge_builder import CartridgeBuilder

class CartridgeSelector(ABC):
    @abstractmethod
    def select(self, builder : CartridgeBuilder):
        pass
