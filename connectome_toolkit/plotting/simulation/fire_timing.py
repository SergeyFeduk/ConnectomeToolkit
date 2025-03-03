import plotly.graph_objects as go

def plot_fire_timings(spike_times, neuron_ids_to_plot, time, tick_percent = 0.02):
    """Creates a raster plot of spike times with specified x-axis range and y-axis tick frequency."""
    fig = go.Figure()

    for i, neuron_id in enumerate(neuron_ids_to_plot):
        spike_times_neuron = spike_times[neuron_id]
        fig.add_trace(go.Scatter(x=spike_times_neuron, y=[i] * len(spike_times_neuron), mode='markers', marker=dict(size=5), name=f'Neuron {neuron_id}'))

    tick_frequency = int(tick_percent * len(neuron_ids_to_plot))

    y_tickvals = list(range(0, len(neuron_ids_to_plot), tick_frequency))
    y_ticktext = [str(neuron_ids_to_plot[i]) for i in y_tickvals]

    fig.update_layout(
        title='Raster Plot of Spiking Activity',
        xaxis_title='Time (ms)',
        yaxis_title='Neuron ID',
        xaxis=dict(range=[0, time[-1]]),
        yaxis=dict(tickvals=y_tickvals, ticktext=y_ticktext)
    )

    return fig