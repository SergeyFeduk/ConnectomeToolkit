import polars as pl
from src.cartridge_builders.filters.cartridge_filter import CartridgeFilter, CartridgeFilterPayload

class CustomFilter(CartridgeFilter):
    def __init__(self, function : callable):
        self.function = function

    def apply(self, payload : CartridgeFilterPayload) -> pl.DataFrame:
        return self.function(payload)
