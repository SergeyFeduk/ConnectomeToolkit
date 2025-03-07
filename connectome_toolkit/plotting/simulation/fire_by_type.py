from collections import defaultdict
import plotly.graph_objects as go

from connectome_toolkit.simulation.data import SpikesSimulationData

def plot_spike_counts_by_type(data : SpikesSimulationData, neuron_types, normalize : bool = False):
    """Plots number of spikes by neuron type."""
    spike_counts = defaultdict(int)
    for neuron_id, spikes in data.spike_times.items():
        neuron_type = neuron_types[neuron_id]
        spike_counts[neuron_type] += len(spikes)
    
    title = 'Total Number of Spikes by Neuron Type'
    if normalize:
        title = 'Normalized Number of Spikes by Neuron Type'
        neuron_type_counts = defaultdict(int)
        for neuron_id in neuron_types:
            neuron_type_counts[neuron_types[neuron_id]] += 1

        for neuron_type in spike_counts:
            if neuron_type in neuron_type_counts and neuron_type_counts[neuron_type] > 0:
                spike_counts[neuron_type] /= neuron_type_counts[neuron_type]

    fig = go.Figure(data=[go.Bar(x=list(spike_counts.keys()), y=list(spike_counts.values()))])
    fig.update_layout(
        title=title,
        xaxis_title='Neuron Type',
        yaxis_title='Number of Spikes'
    )
    return fig