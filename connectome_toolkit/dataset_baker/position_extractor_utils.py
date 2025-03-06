import polars as pl
import re

def preprocess_position_format(position_format : str) -> list[int]:
    components = ['X', 'Y', 'Z']
    component_indices = []
    for component in components:
        try:
            index = position_format.index(component)
            component_indices.append(index)
        except ValueError:
            raise ValueError(f"Position format must contain component: {component}")

    if len(component_indices) != 3:
        raise ValueError(f"Position format must contain exactly X, Y, and Z components")

    component_indices.sort() # Ensure indices are in order X, Y, Z
    return component_indices

def get_delimiters(position_format : str, component_indices : list[int]) -> list[str]:
    delimiters = []
    for i in range(len(component_indices) - 1):
        start_index = component_indices[i] + 1
        end_index = component_indices[i+1]
        delimiter = position_format[start_index:end_index]
        delimiters.append(delimiter)
    return delimiters

def get_non_data_chars_corrected(position_format : str, delimiters : list[str], components : list[str] = ['X', 'Y', 'Z']) -> list[str]:
    non_data_chars = []
    delimiter_str = "".join(delimiters)
    component_str = "".join(components)
    data_chars = delimiter_str + component_str
    for char in position_format:
        if char not in data_chars:
            non_data_chars.append(char)
    return non_data_chars

def escape_regex_chars(text : str) -> str:
    regex_special_chars = re.escape(r'\.[](){}?*+-|^$')
    escaped_string_list = [char if char not in regex_special_chars else '\\' + char for char in text]
    escaped_string = "|".join(escaped_string_list)
    return escaped_string

def remove_x_and_strip(neuron_position_val : str, x_str_val : str, delimiter : str) -> str:
    intermediate_string = neuron_position_val.replace(x_str_val, "", 1)
    return intermediate_string.lstrip(delimiter)

def extract_component(series : pl.Series, delimiter : str, index : int, handle_nulls = False) -> pl.Series:
    split_list = series.str.strip_chars(" ").str.split(delimiter).list.eval(pl.element().str.strip_chars(" ")) #Split and strip string
    if handle_nulls and index == 1: #Special case for Z dimension
        split_list = split_list.list.eval(
             pl.when(pl.element() != "")
             .then(pl.element())
             .otherwise(None)
        ).list.drop_nulls()
    return split_list.list.get(index)