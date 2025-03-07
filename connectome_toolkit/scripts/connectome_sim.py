from connectome_toolkit.serialization import CartridgeSerializer, Cartridge

from connectome_toolkit.simulation.methods import LeakyIntegrateAndFire
from connectome_toolkit.simulation.data import SpikesSimulationData
from connectome_toolkit.simulation.excitation_functions import smooth_bump
from connectome_toolkit.utils import get_synaptic_lookup

from connectome_toolkit.plotting.simulation import plot_fire_timings, plot_spike_counts_by_type, plot_animated_neurons_firing, plot_fire_rate_graph

cartridge : Cartridge = CartridgeSerializer.deserialize("PhotoRN.cartridge")

#Simulation parameters
duration = 100 #In ms
timestep = 0.1

stimulated_types = ['R7', 'R8'] #Photoreceptors
excitation_parameters = {
    'start_point': .2,
    'rise_rate': 2,
    'fade_start': .28,
    'fade_rate': 0.9,
    'amplitude': 10
}
max_synapse_weight = 100
synapse_coefficient = 0.013
#Network Data Structures
neuron_types = {int(i[0]):i[1] for i in cartridge.neuron_type_list}
synapses = get_synaptic_lookup(cartridge.connections_list, max_synapse_weight, synapse_coefficient)
neuron_ids = list(neuron_types.keys())

#Prepare and run simulation
lif = LeakyIntegrateAndFire(smooth_bump, duration, timestep, neuron_ids, synapses, 0)
lif.precompute_excitation(excitation_parameters)
lif.precompute_acceleration_structure(neuron_types, stimulated_types)
lif.run_simulation()

sim_data : SpikesSimulationData = lif.get_data()
# Plot everything
plot_animated_neurons_firing(cartridge, sim_data, 0).show()
plot_fire_timings(neuron_ids, sim_data).show()
plot_spike_counts_by_type(sim_data, neuron_types, True).show()
plot_fire_rate_graph(neuron_ids, sim_data, 5).show()