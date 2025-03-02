from connectome_toolkit.serialization import CartridgeSerializer, Cartridge

from connectome_toolkit.methods import LeakyIntegrateAndFire
from connectome_toolkit.excitation_functions import smooth_bump
from connectome_toolkit.utils import get_synaptic_lookup

from connectome_toolkit.plotting.simulation import plot_fire_timings, plot_spike_counts_by_type, plot_animated_neurons_firing, plot_fire_rate_graph

cartridge : Cartridge = CartridgeSerializer.deserialize("PhotoRN.cartridge")

#Simulation parameters
duration = 100 #In ms
timestep = 0.1

stimulated_types = ['R7', 'R8'] #Photoreceptors
excitation_params = {
    'start_point': .2,
    'rise_rate': 2,
    'fade_start': .28,
    'fade_rate': 0.9,
    'amplitude': 40
}
max_synapse_weight = 100
synapse_coefficient = 0.013
#Network Data Structures
neuron_types = {int(i[0]):i[1] for i in cartridge.neuron_type_list}
synapses = get_synaptic_lookup(cartridge.connections_list, max_synapse_weight, synapse_coefficient)
neuron_ids = list(neuron_types.keys())

lif = LeakyIntegrateAndFire(smooth_bump, duration, timestep, neuron_ids, synapses, 0)
lif.precompute_excitation(excitation_params)
lif.precompute_acceleration_structure(neuron_types, stimulated_types)
lif.run_simulation()

time = lif.time
spike_times = lif.spike_times

# Plot everything
plot_animated_neurons_firing(cartridge.neuron_positions_dict, time, spike_times, 10, 0).show(rendermode="webgl")
plot_fire_timings(spike_times, neuron_ids, time).show(rendermode="webgl")
plot_spike_counts_by_type(spike_times, neuron_types).show(rendermode="webgl")
plot_fire_rate_graph(spike_times, neuron_ids, time, 5).show(rendermode="webgl")