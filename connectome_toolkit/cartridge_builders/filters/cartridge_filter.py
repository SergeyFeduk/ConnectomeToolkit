import polars as pl
from abc import ABC, abstractmethod

class CartridgeFilterPayload:
    def __init__(self, types_data: pl.DataFrame, positions_data: pl.DataFrame, connections_data: pl.DataFrame):
        self.types_data = types_data
        self.positions_data = positions_data
        self.connections_data = connections_data

class CartridgeFilter(ABC):
    @abstractmethod
    def apply(self, payload : CartridgeFilterPayload) -> list[pl.DataFrame] | pl.DataFrame:
        pass
