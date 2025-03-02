class Cartridge():
    def __init__(self, 
                 neuron_type_list : list[list[int, str, str]], 
                 connections_list : list[list[int, int, str, int, str]], 
                 neuron_positions_dict : dict[int, list[int, int, int]]):
        self.neuron_type_list = neuron_type_list
        self.connections_list = connections_list
        self.neuron_positions_dict = neuron_positions_dict
    
    def __str__(self):
        return f"Cartridge (neurons: {len(self.neuron_type_list)}, connections: {len(self.connections_list)})"