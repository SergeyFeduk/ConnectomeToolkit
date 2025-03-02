import os.path
import polars as pl

from connectome_toolkit.serialization import Cartridge

class CartridgeBuilder():
    def __init__(self, dataset_name : str, directory : str = None):
        if not directory:
            directory = "parquet_output"
        self.dataset_name = dataset_name
        self.types_data = self._load_data(os.path.join(directory, f"{dataset_name}_neuron_types.parquet"))
        self.positions_data = self._load_data(os.path.join(directory, f"{dataset_name}_neuron_positions.parquet"), False)
        self.connections_data = self._load_data(os.path.join(directory, f"{dataset_name}_connections.parquet"))

        self.cartridge_types_data = self.types_data.clone()

    def _load_data(self, path, strict = True) -> pl.DataFrame | None:
        if os.path.isfile(path):
            return pl.read_parquet(path)
        else:
            if strict:
                raise FileExistsError(path + " does not exist")
            else:
                return None
            
    def filter(self, filter : "CartridgeFilter", input_data : pl.DataFrame = None) -> list[pl.DataFrame] | pl.DataFrame:
        data_to_filter = input_data if input_data is not None else self.types_data
        payload = CartridgeFilterPayload(data_to_filter, self.positions_data, self.connections_data)
        return filter.apply(payload)
    
    def select(self, selector : "CartridgeSelector") -> None:
        selector.select(self)

    def build_cartridge(self) -> Cartridge:
        #Filter connections
        filtered_neuron_ids = self.cartridge_types_data["neuron_id"].to_list()
        filtered_connections_data = self.connections_data.filter(
            pl.col('neuron_pre').is_in(filtered_neuron_ids) &
            pl.col('neuron_post').is_in(filtered_neuron_ids)
        )
        #Filter positions
        filtered_neuron_positions_dict = None
        if self.positions_data is not None:
            
            filtered_positions_data = self.positions_data.filter(
                pl.col("neuron_id").is_in(filtered_neuron_ids)
            )
            filtered_neuron_positions_dict = {row["neuron_id"] : row["neuron_position"] for row in filtered_positions_data.to_dicts()}
        #Create cartridge
        cartridge = Cartridge(
            self.cartridge_types_data.to_numpy().tolist(),
            filtered_connections_data.to_numpy().tolist(),
            filtered_neuron_positions_dict
        )
        return cartridge

from connectome_toolkit.cartridge_builders.filters import CartridgeFilter, CartridgeFilterPayload
from connectome_toolkit.cartridge_builders.selectors import CartridgeSelector
