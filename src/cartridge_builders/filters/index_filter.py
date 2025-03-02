import polars as pl
from src.cartridge_builders.filters.cartridge_filter import CartridgeFilter, CartridgeFilterPayload

class IndexFilter(CartridgeFilter):
    def __init__(self, target_indices : list[int]):
        self.target_indices = target_indices

    def apply(self, payload : CartridgeFilterPayload):
        data = payload.types_data
        return data.filter(pl.col("neuron_id").is_in(self.target_indices))
