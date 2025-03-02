import polars as pl
from src.cartridge_builders.filters import CartridgeFilter, CartridgeFilterPayload

class NeighbourFilter(CartridgeFilter):
    def __init__(self, neuron_ids: pl.DataFrame):
        self.neuron_ids_df = neuron_ids

    def apply(self, payload: CartridgeFilterPayload) -> pl.DataFrame:
        connections_df = payload.connections_data
        types_df = payload.types_data

        # Find outgoing and incoming connections to the input neurons
        outgoing_connections = connections_df.filter(pl.col("neuron_pre").is_in(self.neuron_ids_df["neuron_id"]))
        incoming_connections = connections_df.filter(pl.col("neuron_post").is_in(self.neuron_ids_df["neuron_id"]))

        # Extract neighbor neuron IDs, exclude original neurons
        neighbor_pre_ids = outgoing_connections["neuron_post"].unique().to_list()
        neighbor_post_ids = incoming_connections["neuron_pre"].unique().to_list()
        neighbor_ids = list(set(neighbor_pre_ids + neighbor_post_ids) - set(self.neuron_ids_df["neuron_id"].to_list()))

        # Get types data for neighbor neurons
        neighbor_types_df = types_df.filter(pl.col("neuron_id").is_in(neighbor_ids))

        return neighbor_types_df
