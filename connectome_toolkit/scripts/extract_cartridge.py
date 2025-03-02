import polars as pl
import numpy as np

from connectome_toolkit.serialization import CartridgeSerializer

from connectome_toolkit.cartridge_builders import CartridgeBuilder
from connectome_toolkit.cartridge_builders.filters import TypeFilter, ClusterFilter, NeighbourFilter
from connectome_toolkit.cartridge_builders.selectors import CombineSelector

from connectome_toolkit.plotting.cartridge import plot_cartridge_3d

builder = CartridgeBuilder("Drosophila_140k")

#Select photoreceptors and cluster them
photoreceptors = builder.filter(TypeFilter(['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']))
photoreceptors_clustered = builder.filter(ClusterFilter(20), photoreceptors)

#Select the cluster with median size
cluster_lengths = [len(cluster) for cluster in photoreceptors_clustered]
median_length = np.median(cluster_lengths)
selected_cluster = min(photoreceptors_clustered, key=lambda cluster: abs(len(cluster) - median_length))

#Select immediate neighbours of selected cluster
photoreceptor_neighbors = builder.filter(NeighbourFilter(selected_cluster))

#Combine and apply data for builder
selected_neurons = pl.concat([selected_cluster, photoreceptor_neighbors])
builder.select(CombineSelector([selected_neurons]))


cartridge = builder.build_cartridge()
print(cartridge)
plot_cartridge_3d(cartridge, False).show()
CartridgeSerializer.serialize("PhotoRN.cartridge", cartridge)
