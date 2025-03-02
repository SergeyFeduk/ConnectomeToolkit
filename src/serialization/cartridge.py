class Cartridge():
    def __init__(self, neuron_type_list, connections_list, neuron_positions_dict):
        self.neuron_type_list = neuron_type_list
        self.connections_list = connections_list
        self.neuron_positions_dict = neuron_positions_dict
    
    def __str__(self):
        return f"Cartridge (neurons: {len(self.neuron_type_list)}, connections: {len(self.connections_list)})"