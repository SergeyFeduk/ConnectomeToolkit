def get_synaptic_sign(nt_type : str) -> float:
    if nt_type == "ACH" or nt_type == "GLUT":
        return 1
    elif nt_type == "GABA":
        return -1
    elif nt_type == None:
        return 1
    else:
        return -1