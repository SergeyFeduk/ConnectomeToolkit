from connectome_toolkit.utils import get_synaptic_sign

def get_synaptic_lookup(loaded_connections_list, max_weight : float, weight_coefficient):
    synapses = {}
    #Iterate each connection
    for pre_id, post_id, _, syn_count, nt_type in loaded_connections_list:
        #Skip unassiged connections
        if syn_count is None:
            continue
        syn_weight = float(min(syn_count, max_weight)) * weight_coefficient
        synapses[(pre_id, post_id)] = (syn_weight, get_synaptic_sign(nt_type))
    return synapses