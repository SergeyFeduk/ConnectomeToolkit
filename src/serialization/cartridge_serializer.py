import pickle
from src.serialization.cartridge import Cartridge

class CartridgeSerializer():
    class SerializationError(Exception):
        """Custom exception raised for cartridge serialization/deserialization errors."""
        pass
    
    def serialize(path : str, cartridge : Cartridge):
        try:
            with open(path, 'wb') as file:
                pickle.dump(cartridge, file)
        except pickle.PicklingError as e:
            raise CartridgeSerializer.SerializationError(f"Failed to save cartridge: {e}")

    def serialize_data(path : str, neuron_type_list, connections_list, neuron_coordinates_dict):
        cartridge = Cartridge(neuron_type_list, connections_list, neuron_coordinates_dict)
        CartridgeSerializer.serialize(cartridge)

    def deserialize(path : str) -> Cartridge:
        try:
            with open(path, 'rb') as file:
                cartridge = pickle.load(file)
                return cartridge
        except FileNotFoundError as e:
            raise CartridgeSerializer.SerializationError(f"Cartridge file not found: {e.filename}")
        except pickle.UnpicklingError as e:
            raise CartridgeSerializer.SerializationError(f"Could not load data from cartridge file. File might be corrupted: {e}")