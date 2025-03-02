import argparse
import yaml
import polars as pl
import os

#Parse arguments
parser = argparse.ArgumentParser(prog = "Dataset baker", description = "Bake any dataset into file compatible with this ConnectomeToolkit")
parser.add_argument("-c", "--config")
parser.add_argument("-o", "--output_dir")
args = parser.parse_args()

output_dir = "parquet_output"
#Load dataset using YAML config
try:
    config_file = args.config
    config = yaml.load(open(config_file, "r"), yaml.CLoader)
    #Validate config
    dataset_config = config['dataset']
    dataset_name = dataset_config['name']
    neurons_config = dataset_config['neurons']
    connections_config = dataset_config['connections']
    #Output directory
    if args.output_dir:
        output_dir = args.output_dir
except FileNotFoundError as e:
    raise FileNotFoundError(f"Did not find config file: {e}")
except KeyError as e:
    raise KeyError(f"Dataset structure if invalid: {e}")

#Read original files
print("Reading files")
type_filepath = neurons_config.get('type_file')
position_filepath = neurons_config.get('position_file', None)
connections_filepath = connections_config.get('connections_file')

type_file = pl.read_csv(type_filepath)
if position_filepath:
    position_file = pl.read_csv(position_filepath)
connections_file = pl.read_csv(connections_filepath)
#Restructure dataframes to map to our data structure
print("Baking dataset")
type_data = type_file.rename({
    neurons_config['type_key_column']: "neuron_id",
    neurons_config['type_column']: "neuron_type"
})
if position_filepath:
    position_data = position_file.rename({
        neurons_config['position_key_column']: "neuron_id",
        neurons_config['position_column']: "neuron_position"
    })
    #TODO: This should be generalized and defined in config
    position_data = position_data.with_columns(
        pl.col("neuron_position")
        .str.replace_all(r"\[|\]", "") #Remove brackets
        .str.strip_chars(" ") #Remove trailing spaces
        .str.replace_all(r"\s+", " ") #Remove excessive intermediate spaces
        .str.split(" ") #Split by spaces
        .list.eval(pl.element().cast(pl.Int32)) #Convert to integers
        .alias("neuron_position")
    )
    
connections_data = connections_file.rename({
    connections_config['pre_column']: "neuron_pre",
    connections_config['post_column']: "neuron_post",
    connections_config['weights_column']: "connection_weight",
    connections_config['sign_column']: "connection_sign",
})

#Save data as parquet files
print("Saving dataset")
os.makedirs(output_dir, exist_ok=True)

type_data.write_parquet(os.path.join(output_dir, f"{dataset_name}_neuron_types.parquet"))
if position_filepath:
    position_data.write_parquet(os.path.join(output_dir, f"{dataset_name}_neuron_positions.parquet"))
connections_data.write_parquet(os.path.join(output_dir, f"{dataset_name}_connections.parquet"))