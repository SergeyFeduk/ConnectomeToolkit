import polars as pl
from connectome_toolkit.cartridge_builders.selectors.cartridge_selector import CartridgeSelector

class CombineSelector(CartridgeSelector):
    def __init__(self, neuron_frames : list[pl.DataFrame]):
        self.neuron_frames = neuron_frames
    def select(self, builder : "CartridgeBuilder") -> None:
        builder.cartridge_types_data = pl.concat(self.neuron_frames)