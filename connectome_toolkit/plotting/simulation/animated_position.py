import plotly.graph_objects as go
import numpy as np

from connectome_toolkit.simulation.data import SpikesSimulationData

def plot_animated_neurons_firing(loaded_neuron_coordinates_dict, data : SpikesSimulationData, skip_frames : int= 0):
    neuron_positions = []
    neuron_ids_for_plotting = []
    frame_duration = 10

    for root_id, position_list in loaded_neuron_coordinates_dict.items():
        neuron_ids_for_plotting.append(root_id)
        neuron_positions.append(position_list)

    neuron_positions_np = np.array(neuron_positions)
    color_timesteps = []
    for t_index in range(len(data.time)):
        colors = np.zeros(len(neuron_positions))
        for neuron_idx, neuron_id in enumerate(neuron_ids_for_plotting):
            if data.time[t_index] in data.spike_times[neuron_id]:
                colors[neuron_idx] = 1
        color_timesteps.append(colors)

    num_nodes = neuron_positions_np.shape[0]
    num_timesteps = len(color_timesteps)

    if not all(color_timestep.shape == (num_nodes,) for color_timestep in color_timesteps):
        raise ValueError("Each color_timesteps array must have shape (N,), where N is the number of nodes.")

    fig = go.Figure(data=[go.Scatter3d(
        x=neuron_positions_np[:, 0],
        y=neuron_positions_np[:, 1],
        z=neuron_positions_np[:, 2],
        mode='markers',
        marker=dict(
            size=8,
            color=color_timesteps[0],
            colorscale='Viridis',
            opacity=0.8
        ),
        name='Nodes'
    )])

    frames = []
    for i in range(num_timesteps):
        frame = go.Frame(data=[go.Scatter3d(
            marker=dict(
                color=color_timesteps[i]
            )
        )],
        name=f'frame_{i}'
        )
        frames.append(frame)

    fig.frames = frames

    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 16},
            'prefix': 'Time:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': frame_duration, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }

    for i in range(0, num_timesteps, skip_frames + 1):
        step = {
            'method': 'animate',
            'args': [[f'frame_{i}'],
                        {'frame': {'duration': frame_duration, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 1}}
                        ],
            'label': str(i)
        }
        sliders_dict['steps'].append(step)


    fig.update_layout(
        sliders=[sliders_dict],
        updatemenus=[{
            'type': 'buttons',
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [
                    [f'frame_{i}' for i in range(0, num_timesteps, skip_frames + 1)],
                    {'frame': {'duration': frame_duration, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 0, 'easing': 'linear'}}
                ]
            }, {
                'label': 'Pause',
                'method': 'animate',
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                    'transition': {'duration': 0}}]
            }]
        }],

        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'),
        title='Animated firing scatter'
    )
    return fig