import polars as pl
from connectome_toolkit.dataset_baker.position_extractor_utils import *

def extract_positions(position_file : pl.DataFrame, neurons_config : dict) -> pl.DataFrame:
    #Process position format to find delimiters and non-data chars
    position_format = neurons_config.get('position_column_format', "[X Y Z]")
    component_indices = preprocess_position_format(position_format)
    delimiters = get_delimiters(position_format, component_indices)
    non_data_chars_str = "".join(get_non_data_chars_corrected(position_format, delimiters))

    #Unify position dataframe and drop unused columns
    position_data = position_file.rename({
        neurons_config['position_key_column']: "neuron_id",
        neurons_config['position_column']: "neuron_position"
    }).select(["neuron_id", "neuron_position"]).with_columns( #Remove non-data characters
        pl.col("neuron_position")
        .str.replace_all(escape_regex_chars(non_data_chars_str), "")
    )

    #Extract X column
    position_data = position_data.with_columns(
        x = extract_component(pl.col("neuron_position"), delimiters[0], 0).alias("x")
    )

    #Extract YZ substring
    position_data = position_data.with_columns(
        pl.struct('neuron_position','x').map_elements(
            function=lambda x: 
                remove_x_and_strip(x['neuron_position'], x['x'], delimiters[0]), return_dtype = pl.String
        ).alias("yz")
    )

    #Extract Y and Z columns
    position_data = position_data.with_columns(
        y = extract_component(pl.col("yz"), delimiters[1], 0).alias("y"),
        z = extract_component(pl.col("yz"), delimiters[1], 1, True).alias("z")
    )

    #Create a list of integer positions, drop unused columns
    position_data = position_data.with_columns(
        pl.concat_list([
            pl.col("x").cast(pl.Int32),
            pl.col("y").cast(pl.Int32),
            pl.col("z").cast(pl.Int32)
        ]).alias("neuron_position")
    ).select(["neuron_id", "neuron_position"])

    return position_data