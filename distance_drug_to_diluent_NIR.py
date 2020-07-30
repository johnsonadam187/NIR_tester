import pandas as pd
import numpy as np
from file_IO import file_in, file_path_to_df
from PyQt5.QtWidgets import  QApplication
import sys

"""Checks distance diluent to drug at a specific conc and wavelength. Input list of wavelengths 
into the main function, and specify diluent identity"""

def file_load():
    file_path =  file_in()
    df1 =file_path_to_df(file_path)
    return df1

def filter_df_by_columns(dataframe, conc_string):
    mask = dataframe.columns.str.contains(conc_string)
    dataframe = dataframe[dataframe.columns[mask]].copy()
    return dataframe


def get_value_at_wavelength(dataframe, wavelength):
    wave_length = dataframe[(dataframe.index > wavelength) & (dataframe.index < (wavelength+ 1))]
    wavelength_mean = wave_length.mean(axis=1)
    wavelength_mean = wavelength_mean.mean()
    return wavelength_mean


def iterate_value_at_wavelength(dataframe, wavelength_list):
    output = {}
    for i in range(len(wavelength_list)):
        wave_mean = get_value_at_wavelength(dataframe, wavelength_list[i])
        output[i] = wave_mean
    return output


def calculate_difference(diluent_value, drug_value):
    difference = np.abs(diluent_value - drug_value)
    return difference


def iterate_difference(diluent_values_dict, drug_values_dict):
    collection = {}
    for i in range(len(diluent_values_dict)):
        value = calculate_difference(diluent_values_dict[i], drug_values_dict[i])
        collection[i] = value
    return collection

def print_results(results, col_list):
    print("Absolute distance Drug to Diluent")
    for i in range(len(results)):
        print(f"{col_list[i]} nm : {results[i]}")


def main(wavelength_list):
    col_list = wavelength_list
    df1 = file_load()
    df2 = filter_df_by_columns(df1, "Saline")
    diluent_values = iterate_value_at_wavelength(df2, wavelength_list)
    df3 = filter_df_by_columns(df1, "60")
    drug_values = iterate_value_at_wavelength(df3, wavelength_list)
    results = iterate_difference(diluent_values, drug_values)
    print_results(results, col_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main([1310, 1387, 1550, 1654, 1670, 1749, 1850])
    sys.exit(app.exec_())