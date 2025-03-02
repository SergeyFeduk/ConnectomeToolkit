from connectome_toolkit.serialization import Cartridge
import plotly.graph_objects as go

def plot_cartridge_3d(cartridge : Cartridge, show_connections : bool = True, connections_opacity : float = 0.1):
    neuron_scatter = {
        'x': [], 'y': [], 'z': [],
        'mode': 'markers', 'marker': {'color': 'blue', 'size': 5}, 'name': 'Neurons'
    }

    for _, position_list in cartridge.neuron_positions_dict.items():
        x, y, z = position_list[0], position_list[1], position_list[2]
        neuron_scatter['x'].append(x)
        neuron_scatter['y'].append(y)
        neuron_scatter['z'].append(z)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(neuron_scatter))
    
    title = "Neuron positions"
    if show_connections:
        connection_lines = {
            'x': [], 'y': [], 'z': [],
            'mode': 'lines', 'line': {'color': 'red', 'width': 1}, 'opacity': connections_opacity, 'name': 'Connections'
        }
        neuron_coordinates = cartridge.neuron_positions_dict.keys()
        for pre_neuron_id, post_neuron_id, _, _, _ in cartridge.connections_list:
            if pre_neuron_id in neuron_coordinates and post_neuron_id in neuron_coordinates:
                pre_pos = cartridge.neuron_positions_dict[pre_neuron_id]
                post_pos = cartridge.neuron_positions_dict[post_neuron_id]
                pre_x, pre_y, pre_z = pre_pos[0], pre_pos[1], pre_pos[2]
                post_x, post_y, post_z = post_pos[0], post_pos[1], post_pos[2]
                if all(coord is not None for coord in [pre_x, pre_y, pre_z, post_x, post_y, post_z]):
                    connection_lines['x'].extend([pre_x, post_x, None])
                    connection_lines['y'].extend([pre_y, post_y, None])
                    connection_lines['z'].extend([pre_z, post_z, None])

        title = "Neuron positions and connections"
        fig.add_trace(go.Scatter3d(connection_lines))
        
    fig.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        title=title, showlegend=False
    )
    return fig