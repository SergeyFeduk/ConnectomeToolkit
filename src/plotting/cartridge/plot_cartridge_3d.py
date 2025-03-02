from src.serialization.cartridge import Cartridge
import plotly.graph_objects as go

def plot_cartridge_3d(cartridge : Cartridge, show_connections : bool = True):
    neuron_scatter = {
        'x': [], 'y': [], 'z': [],
        'mode': 'markers', 'marker': {'color': 'blue', 'size': 5}, 'name': 'Neurons'
    }
    for neuron_id, position_list in cartridge.neuron_positions_dict.items():
        x,y,z = position_list[0], position_list[1], position_list[2]
        neuron_scatter['x'].append(x)
        neuron_scatter['y'].append(y)
        neuron_scatter['z'].append(z)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(neuron_scatter))
    fig.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        title='Cartridge positions', showlegend=False
    )
    return fig