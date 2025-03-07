from .simulation_data import SimulationData

class SpikesSimulationData(SimulationData):
    def __init__(self, neuron_ids : list[int]):
        self.spike_times = {neuron_id : [] for neuron_id in neuron_ids}