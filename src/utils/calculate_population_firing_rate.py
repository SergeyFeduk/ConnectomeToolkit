def calculate_population_firing_rate(spike_times, neuron_ids, time, window_size_ms = 10):
    firing_rates = []
    time_points = []
    num_neurons = len(neuron_ids)
    window_size_sec = window_size_ms / 1000.0  # Convert window size to seconds

    for t in time[:-1]: # Iterate up to the second to last time point to define windows
        window_start = t
        window_end = t + window_size_ms
        window_center_time = (window_start + window_end) / 2.0
        total_spikes_in_window = 0

        for neuron_id in neuron_ids:
            spikes_in_window = [spike_time for spike_time in spike_times[neuron_id] if window_start <= spike_time < window_end]
            total_spikes_in_window += len(spikes_in_window)

        # Calculate firing rate in Hz
        population_rate = total_spikes_in_window / (num_neurons * window_size_sec) if num_neurons > 0 and window_size_sec > 0 else 0
        firing_rates.append(population_rate)
        time_points.append(window_center_time)

    return time_points, firing_rates