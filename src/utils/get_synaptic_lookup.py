from src.utils.get_synaptic_sign import get_synaptic_sign

def get_synaptic_lookup(loaded_connections_list, max_weight : float, weight_coefficient):
    synapses = {}
    for pre_id, post_id, _, syn_count, nt_type in loaded_connections_list:
        if syn_count is None or syn_count > max_weight:
            syn_count = min(syn_count, max_weight)
        synapses[(pre_id, post_id)] = (min(float(syn_count) * weight_coefficient, 1), get_synaptic_sign(nt_type))
    return synapses