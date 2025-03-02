import polars as pl
from src.cartridge_builders.filters import CartridgeFilter, CartridgeFilterPayload
from sklearn.cluster import KMeans
import numpy as np

class ClusterFilter(CartridgeFilter):
    def __init__(self, clusters_count: int, random_state : int = 0):
        self.clusters_count = clusters_count
        self.random_state = random_state

    def apply(self, payload : CartridgeFilterPayload) -> list[pl.DataFrame]:
        positions_df = payload.positions_data
        types_df = payload.types_data

        if positions_df is None:
            raise ValueError("Positions dataframe is not present, clustering is impossible")

        positions = np.array(positions_df["neuron_position"].to_list())

        if len(positions) == 0:
            raise ValueError("Positions dataframe is empty, clustering is impossible")

        #Clusterize data
        kmeans = KMeans(n_clusters=self.clusters_count, random_state = self.random_state, n_init=10)
        kmeans.fit(positions)
        labels = kmeans.labels_

        #Obtain neuron_ids
        cluster_ids = np.unique(labels)
        for cluster_id in cluster_ids:
            cluster_neuron_indices = np.where(labels == cluster_id)[0]
            neuron_ids_in_cluster = positions_df["neuron_id"].gather(cluster_neuron_indices)

        #Obtain dataframes and remove empty clusters
        cluster_dataframes : list[pl.DataFrame] = []
        for cluster_id in cluster_ids:
            cluster_neuron_indices = np.where(labels == cluster_id)[0]
            neuron_ids_in_cluster = positions_df["neuron_id"].gather(cluster_neuron_indices)
            cluster_df = types_df.filter(pl.col("neuron_id").is_in(neuron_ids_in_cluster))
            if len(cluster_df) != 0:
                cluster_dataframes.append(cluster_df)

        return cluster_dataframes
