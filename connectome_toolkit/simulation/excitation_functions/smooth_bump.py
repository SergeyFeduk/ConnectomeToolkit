import numpy as np

def smooth_bump(t_val : float, start_point : float = .2, rise_rate : float = 2, 
                fade_start : float = .3, fade_rate : float = 0.5, amplitude : float = 40):
    sigmoid_start = 1 / (1 + np.exp(-2 * (t_val - start_point)))
    rise_factor = np.exp(rise_rate * 100 * (t_val - start_point)) * sigmoid_start
    rise_factor = rise_factor / (1 + rise_factor)
    fade_factor = 1 / (1 + np.exp(fade_rate * 100 * (t_val - fade_start)))
    return amplitude * rise_factor * fade_factor