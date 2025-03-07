import plotly.graph_objects as go
from connectome_toolkit.utils import calculate_population_firing_rate

from connectome_toolkit.simulation.data import SpikesSimulationData

def plot_fire_rate_graph(neuron_ids, data : SpikesSimulationData, window_size_ms = 5):
    time_points_fr, firing_rates = calculate_population_firing_rate(data.spike_times, neuron_ids, data.time, window_size_ms)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_points_fr, y=firing_rates, mode='lines', name='Population Firing Rate'))

    fig.update_layout(
        title='Population Firing Rate Over Time',
        xaxis_title='Time (ms)',
        yaxis_title='Firing Rate (Hz)',
        yaxis_range=[0, max(firing_rates)]
    )

    return fig