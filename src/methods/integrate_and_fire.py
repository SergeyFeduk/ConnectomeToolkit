import random
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from src.methods import SimulationMethod

class LeakyIntegrateAndFireParameters():
    def __init__(self, rest_voltage : float = -70, membrane_resistance : float = 10, tau_membrane : float = 10, 
                 threshold_voltage : float = -55, reset_voltage : float = -75, tau_synaptic : float = 2, reversal_potential : float = 0):
        self.rest_voltage = rest_voltage
        self.membrane_resistance = membrane_resistance
        self.tau_membrane = tau_membrane #In ms
        self.threshold_voltage = threshold_voltage
        self.reset_voltage = reset_voltage
        self.tau_synaptic = tau_synaptic #In ms
        self.reversal_potential = reversal_potential

class LeakyIntegrateAndFire(SimulationMethod):
    MAX_CURRENT = 1e6
    MAX_SYNAPTIC_CONDUCTANCE = 5.0

    def __init__(self, excitation_function : callable, duration : float, timestep : float, neuron_ids : list[int], synapses : dict[tuple[int,int],tuple[float, float]], 
                 randomized_voltage : float = 15, parameters : LeakyIntegrateAndFireParameters = LeakyIntegrateAndFireParameters()):
        super().__init__(excitation_function, duration, timestep)
        #Data
        self.neuron_ids = neuron_ids
        self.synapses = synapses
        self.parameters = parameters
        #Acceleration structure
        self.stimulated_indices = set()
        self.pre_to_post = defaultdict(list)
        self.post_to_pre = defaultdict(list)
        self.neuron_id_to_index = {neuron_id: index for index, neuron_id in enumerate(self.neuron_ids)}
        self.index_to_neuron_id = {index: neuron_id for index, neuron_id in enumerate(self.neuron_ids)}
        self.processed_synapses = defaultdict(list)
        #Simulation arrays
        self.voltage = {neuron_id : np.zeros(len(self.time)) for neuron_id in neuron_ids}
        for neuron_id in neuron_ids:
            self.voltage[neuron_id][0] = self.parameters.rest_voltage + random.uniform(0,randomized_voltage) #Apply randomized initial voltage
        self.g_syn = {neuron_id : np.zeros(len(self.time)) for neuron_id in neuron_ids}
        #Collected data
        self.spike_times = {neuron_id : [] for neuron_id in neuron_ids}

    def precompute_acceleration_structure(self, neuron_types : dict[int, str], stimulated_types : list[str]):
        for neuron_id in self.neuron_ids:
            if neuron_types[neuron_id] in stimulated_types:
                self.stimulated_indices.add(neuron_id)

        for (pre_id, post_id), (_, _) in self.synapses.items():
            self.pre_to_post[pre_id].append(post_id)
            self.post_to_pre[post_id].append(pre_id)

        for (pre_id, post_id), (syn_weight, syn_sign) in tqdm(self.synapses.items(), desc = "Processing Synapses"):
            if post_id in self.neuron_id_to_index and pre_id in self.neuron_id_to_index:
                post_neuron_index = self.neuron_id_to_index[post_id]
                pre_neuron_index = self.neuron_id_to_index[pre_id]
                self.processed_synapses[post_neuron_index].append((pre_neuron_index, syn_weight, syn_sign))

    def step(self, iteration : int, excitation_value : float):
        for neuron_index in range(len(self.neuron_ids)): # Iterate over neuron indices
            neuron_id = self.index_to_neuron_id[neuron_index] # Get neuron_id from index
            V_current = self.voltage[neuron_id][iteration] # Access V using neuron_id (or neuron_index if you change V to be indexed by index)
            V_current = max(min(V_current, LeakyIntegrateAndFire.MAX_CURRENT), -LeakyIntegrateAndFire.MAX_CURRENT)
            synaptic_current = 0

            if neuron_index in self.processed_synapses: # Check if neuron_index has pre-synapses (optional, but good practice)
                pre_synapse_list = self.processed_synapses[neuron_index] # Access using neuron_index

                for _, syn_weight_magnitude, synapse_sign in pre_synapse_list: # Iterate pre-synapses
                    if synapse_sign >= 0:
                        e_rev_syn = 0.0
                    else:
                        e_rev_syn = self.parameters.rest_voltage
                    current_contribution = syn_weight_magnitude * self.g_syn[neuron_id][iteration] * (V_current - e_rev_syn)
                    synaptic_current += current_contribution
            #External input
            if neuron_id in self.stimulated_indices:
                I_excitation_value = excitation_value
            else:
                I_excitation_value = 0
            #Integrate
            dV_unscaled = self.parameters.rest_voltage - V_current + self.parameters.membrane_resistance * I_excitation_value + self.parameters.membrane_resistance * -synaptic_current
            dV = dV_unscaled / self.parameters.tau_membrane * self.timestep
            self.voltage[neuron_id][iteration+1] = V_current + dV
            #Apply decay
            dg_syn = (-self.g_syn[neuron_id][iteration] / self.parameters.tau_synaptic) * self.timestep
            self.g_syn[neuron_id][iteration+1] = self.g_syn[neuron_id][iteration] + dg_syn
            #Check for spike
            if self.voltage[neuron_id][iteration+1] >= self.parameters.threshold_voltage:
                self.spike_times[neuron_id].append(self.time[iteration+1])
                self.voltage[neuron_id][iteration+1] = self.parameters.reset_voltage

                #Update g_syn of post neurons
                for post_neuron_id in self.pre_to_post[neuron_id]:
                    synapse_post = self.synapses[(neuron_id, post_neuron_id)]
                    self.g_syn[post_neuron_id][iteration+1] += synapse_post[0] * synapse_post[1]
                    self.g_syn[post_neuron_id][iteration+1] = min(self.g_syn[post_neuron_id][iteration+1], LeakyIntegrateAndFire.MAX_SYNAPTIC_CONDUCTANCE)