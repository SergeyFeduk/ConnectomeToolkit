import yaml

class DatasetConfig():
    def __init__(self, dataset : dict, neurons : dict, connections : dict):
        self.dataset = dataset
        self.neurons = neurons
        self.connections = connections

    def load(file_path : str) -> "DatasetConfig":
        try:
            config_file = file_path
            config = yaml.load(open(config_file, "r"), yaml.CLoader)
            return DatasetConfig(config['dataset'], config['dataset']['neurons'], config['dataset']['connections'])
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Did not find config file: {e}")
        except KeyError as e:
            raise KeyError(f"Dataset structure if invalid: {e}")