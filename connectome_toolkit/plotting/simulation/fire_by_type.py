from collections import defaultdict
import plotly.graph_objects as go

from connectome_toolkit.simulation.data import SpikesSimulationData

def plot_spike_counts_by_type(data : SpikesSimulationData, neuron_types):
  """Plots the total number of spikes by neuron type."""
  spike_counts = defaultdict(int)
  for neuron_id, spikes in data.spike_times.items():
      neuron_type = neuron_types[neuron_id]
      spike_counts[neuron_type] += len(spikes)

  fig = go.Figure(data=[go.Bar(x=list(spike_counts.keys()), y=list(spike_counts.values()))])
  fig.update_layout(
      title='Total Number of Spikes by Neuron Type',
      xaxis_title='Neuron Type',
      yaxis_title='Number of Spikes'
  )
  return fig