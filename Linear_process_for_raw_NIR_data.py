import pandas as pd
import numpy as np
from file_IO import file_in, file_path_to_df, dataframe_save_to_csv
from linear_analysis import linear_analysis
from PyQt5.QtWidgets import QApplication
import sys
from analyse_nir_data import calculate_variance, average_df_columns
from linear_analysis import linear_analysis
""" Step 4)Whole process automation of NIR data to Linear regression. Goes through entire process from file importation
, replicate averaging, removal of diluent, """

def file_process():
    """ import file process to df"""
    file_path = file_in()
    dataframe = file_path_to_df(file_path)
    return dataframe


def remove_diluent(dataframe, diluent_string):
    mask = dataframe.columns.str.contains(diluent_string)
    drug_mask = [not item for item in mask]
    drug_only_df = dataframe[dataframe.columns[drug_mask]]
    return drug_only_df


def variance_calc(dataframe):
    """Calculate variance of all concentrations for spectrum"""
    variance_at_each_conc = calculate_variance(dataframe)
    return variance_at_each_conc


def average_columns(dataframe):
    averaged_df = average_df_columns(dataframe)
    return averaged_df


def reduce_to_MVP_wavelengths(dataframe, variance_df, wavelength_list):
    collection ={}
    variance_collection = {}
    for num in range(len(wavelength_list)):
        name = wavelength_list[num]
        wave_length = dataframe[(dataframe.index > wavelength_list[num]) &
                                (dataframe.index < (wavelength_list[num] + 1))].mean()
        var_at_wave = variance_df[(variance_df.index > wavelength_list[num]) &
                                (variance_df.index < (wavelength_list[num] + 1))].mean()
        collection[name] = wave_length
        variance_collection[name] = var_at_wave
    data = pd.DataFrame.from_dict(collection)
    variance = pd.DataFrame.from_dict(variance_collection)
    return data, variance


def run_linearity_for_dataframe(dataframe):
    collection = {}
    conc_list = [float(item) for item in dataframe.columns]
    for index, item in enumerate(dataframe.columns):
        series_name = dataframe.columns[index]
        series = dataframe.iloc[:, index]
        m, c, r2 = linear_analysis(series, conc_list)
        collection[series_name] = (m, c, r2)
    linearity_df = pd.DataFrame.from_dict(collection)
    linearity_df.index = ["Coefficient", "Intercept", "R squared"]
    return linearity_df


def file_save(dataframe):
    dataframe_save_to_csv(dataframe)


def main():
    """Must enter hardcoded variables, Diluent name, and laser_wavelengths"""
    df1 = file_process()
    variance = variance_calc(df1)
    drug_only_all_reps = remove_diluent(df1, "Saline")
    variance_drug_conc = variance_calc(drug_only_all_reps)
    avg_df = average_columns(drug_only_all_reps)
    drug_at_lasers, var_at_lasers = reduce_to_MVP_wavelengths(avg_df, variance, [1310, 1387, 1550, 1654, 1670, 1749, 1850])
    linearity_data = run_linearity_for_dataframe(drug_at_lasers)
    return linearity_data, variance


if __name__ == "__main__":
    app = QApplication(sys.argv)
    linearity, variance = main()
    print(linearity.to_string())
    print(variance.to_string())
    # file_save(linearity)
    # file_save(variance)
    sys.exit(app.exec_())
