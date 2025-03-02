import numpy as np
import plotly.graph_objects as go

def _parse_coordinates(position_str, neuron_id=None, connection=None):
    """Helper function to parse coordinate string and handle errors."""
    try:
        coords_str_list = position_str.strip('[]').split()
        x, y, z = map(int, coords_str_list)
        if not np.isfinite(x) or not np.isfinite(y) or not np.isfinite(z):
            raise ValueError("Non-finite coordinates")
        return x, y, z
    except ValueError as e:
        if neuron_id is not None:
            print(f"Warning: Invalid coordinates for neuron ID {neuron_id}: {position_str}. Skipping neuron. Error: {e}")
        elif connection is not None:
            print(f"Warning: Invalid coordinates for synapse between {connection}. Skipping synapse. Error: {e}")
        else:
            print(f"Warning: Invalid coordinate format: {position_str}. Skipping. Error: {e}")
        return None, None, None


def plot_static_neuron_positions(neuron_coordinates, connections, synapse_opacity=0.1):
    """
    Plots static 3D positions of neurons and their synaptic connections.

    Args:
        neuron_coordinates (dict): Dictionary where keys are neuron IDs and values are coordinate strings (e.g., "[10 20 30]").
        connections (list): List of tuples, where each tuple represents a connection (pre-synaptic_neuron_id, post_synaptic_neuron_id).
        synapse_opacity (float, optional): Opacity of synapse lines. Defaults to 0.1.

    Returns:
        plotly.graph_objects.Figure: The Plotly Figure object.
    """
    fig = go.Figure()

    neuron_scatter = {
        'x': [], 'y': [], 'z': [],
        'mode': 'markers', 'marker': {'color': 'blue', 'size': 5}, 'name': 'Neurons'
    }
    synapse_lines = {
        'x': [], 'y': [], 'z': [],
        'mode': 'lines', 'line': {'color': 'red', 'width': 1}, 'opacity': synapse_opacity, 'name': 'Synapses'
    }

    for neuron_id, position_str in neuron_coordinates.items():
        x, y, z = _parse_coordinates(position_str, neuron_id=neuron_id)
        if x is not None:
            neuron_scatter['x'].append(x)
            neuron_scatter['y'].append(y)
            neuron_scatter['z'].append(z)

    for pre_neuron_id, post_neuron_id in connections:
        if pre_neuron_id in neuron_coordinates and post_neuron_id in neuron_coordinates:
            pre_pos_str = neuron_coordinates[pre_neuron_id]
            post_pos_str = neuron_coordinates[post_neuron_id]

            pre_x, pre_y, pre_z = _parse_coordinates(pre_pos_str, connection=(pre_neuron_id, post_neuron_id))
            post_x, post_y, post_z = _parse_coordinates(post_pos_str, connection=(pre_neuron_id, post_neuron_id))

            if all(coord is not None for coord in [pre_x, pre_y, pre_z, post_x, post_y, post_z]):
                synapse_lines['x'].extend([pre_x, post_x, None])
                synapse_lines['y'].extend([pre_y, post_y, None])
                synapse_lines['z'].extend([pre_z, post_z, None])

    fig.add_trace(go.Scatter3d(neuron_scatter))
    fig.add_trace(go.Scatter3d(synapse_lines))
    fig.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        title='Neuron Positions and Synapses', showlegend=True
    )
    return fig