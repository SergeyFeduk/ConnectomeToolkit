import numpy as np
from tqdm import tqdm

class SimulationMethod():
    def __init__(self, excitation_function : callable, duration : float, timestep : float):
        self.excitation_function = excitation_function
        self.time = np.arange(0, duration, timestep)
        self.timestep = timestep

        self.excitation_data = []

    def precompute_excitation(self, params):
        for i in tqdm(range(len(self.time)-1), desc = "Precomputing excitation values"):
            time_percent = self.time[i] / self.time[-1]
            excitation_value = self.excitation_function(time_percent, **params)
            self.excitation_data.append(excitation_value)

    def run_simulation(self):
        if len(self.excitation_data) == 0:
            raise ValueError("Error: Excitation data is not precomputed")
        for i in tqdm(range(len(self.time)-1), desc = "Running simulation"):
            self.step(i, self.excitation_data[i])

    def step(self, iteration : int, excitation_value : float):
        pass