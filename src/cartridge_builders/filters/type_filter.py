import polars as pl
from src.cartridge_builders.filters import CartridgeFilter, CartridgeFilterPayload

class TypeFilter(CartridgeFilter):
    def __init__(self, target_types : list[str]):
        self.target_types = target_types

    def apply(self, payload : CartridgeFilterPayload) -> pl.DataFrame:
        data = payload.types_data
        return data.filter(pl.col("neuron_type").is_in(self.target_types))
