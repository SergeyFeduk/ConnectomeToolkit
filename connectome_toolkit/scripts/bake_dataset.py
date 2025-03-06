import polars as pl
import argparse
import os

from connectome_toolkit.dataset_baker import DatasetConfig, extract_positions, extract_connections

#Parse arguments
parser = argparse.ArgumentParser(prog = "Dataset baker", description = "Bake any dataset into file compatible with ConnectomeToolkit")
parser.add_argument("-c", "--config")
parser.add_argument("-o", "--output_dir")
args = parser.parse_args()

output_dir = "parquet_output"
if args.output_dir:
        output_dir = args.output_dir
config : DatasetConfig = DatasetConfig.load(args.config)
dataset_name = config.dataset["name"]

#Read original files
print("Reading files")
type_filepath = config.neurons.get('type_file')
position_filepath = config.neurons.get('position_file', None)
connections_filepath = config.connections.get('connections_file')

type_file = pl.read_csv(type_filepath)
if position_filepath:
    position_file = pl.read_csv(position_filepath)
connections_file = pl.read_csv(connections_filepath)
#Restructure dataframes to map to our data structure
print("Baking dataset")
type_data = type_file.rename({
    config.neurons['type_key_column']: "neuron_id",
    config.neurons['type_column']: "neuron_type"
})
if position_filepath:
    position_data = extract_positions(position_file, config.neurons)
connections_data = extract_connections(connections_file, config.connections)

#Save data as parquet files
print("Saving dataset")
os.makedirs(output_dir, exist_ok=True)

type_data.write_parquet(os.path.join(output_dir, f"{dataset_name}_neuron_types.parquet"))
if position_filepath:
    position_data.write_parquet(os.path.join(output_dir, f"{dataset_name}_neuron_positions.parquet"))
connections_data.write_parquet(os.path.join(output_dir, f"{dataset_name}_connections.parquet"))