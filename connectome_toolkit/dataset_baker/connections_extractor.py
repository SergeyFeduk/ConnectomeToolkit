import polars as pl

def extract_connections(connections_file : pl.DataFrame, connections_config : dict):
    #Unify connections dataframe
    connections_data = connections_file.rename({
        connections_config['pre_column']: "neuron_pre",
        connections_config['post_column']: "neuron_post",
        connections_config['weights_column']: "connection_weight",
        connections_config['neurotransmitter_column']: "connection_sign",
    })

    #Process neurotransmitter column
    if connections_config['neurotransmitter_format'] == "number":
        connections_data = connections_data.with_columns(
            pl.col("connection_sign").cast(pl.Float32).fill_null(0.0)
        )
    elif connections_config['neurotransmitter_format'] == "name":
        neurotransmitter_mapping = connections_config['neurotransmitter_mapping']
        connections_data = connections_data.with_columns(
            pl.col("connection_sign").replace(neurotransmitter_mapping).fill_null(0.0).cast(pl.Float32)
        )
    else:
        raise ValueError("Configuration has wrong neurotransmitter_format value. It can be either \"number\" or \"name\"")

    return connections_data