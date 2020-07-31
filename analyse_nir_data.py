import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from statistics import variance
from PyQt5.QtWidgets import QApplication
import sys
from file_IO import file_in, file_path_to_df
from linear_analysis import linear_analysis


def nir_data_to_dataframe():
    """uses file dialog to import file to dataframe"""
    filepath = file_in()
    df_obj = file_path_to_df(filepath)
    return df_obj


def calculate_variance(dataframe):
    """calculates variance for each column across entire spectrum"""
    column_groups_list = [item[:4] for item in dataframe.columns]
    unique_array = np.unique(column_groups_list)
    output_dict = {}
    for index, item in enumerate(unique_array):
        mask = dataframe.columns.str.contains(unique_array[index])
        new_series = dataframe[dataframe.columns[mask]].var(axis=1)
        output_dict[item] = new_series
    output_df = pd.DataFrame.from_dict(output_dict)
    return output_df


def plot_full_spectra(dataframe, title_string, legend_state=False):
    """basic plotting for full spectral data"""
    dataframe.plot(legend=legend_state, title=title_string)
    plt.show()


def average_df_columns(dataframe):
    """takes in full values df and groups by column name then averages each column group"""
    column_groups_list = [item[:4] for item in dataframe.columns]
    unique_array = np.unique(column_groups_list)
    output_dict = {}
    for index, item in enumerate(unique_array):
        mask = dataframe.columns.str.contains(unique_array[index])
        new_series = dataframe[dataframe.columns[mask]].mean(axis=1)
        output_dict[item] = new_series
    output_df = pd.DataFrame.from_dict(output_dict)
    return output_df


def remove_diluent_values(dataframe, diluent_id_string):
    """takes in dataframe of averaged values for different concentrations and diluent, separates diluent"""
    diluent_string = diluent_id_string[:4]
    diluent_col = dataframe[diluent_string]
    avg_drug_only_df = dataframe.drop(diluent_string, axis=1)
    return diluent_col, avg_drug_only_df


def calculate_distance_from_diluent(dataframe, diluent_series):
    """Subtracts distance to diluent values for each column"""
    distance_to_diluent = dataframe.subtract(diluent_series, axis=0)
    return distance_to_diluent


def normalise_data(dataframe, normalise_series):
    """Divides each column by its corresponding value in the normalising series"""
    normalised_df = dataframe.divide(normalise_series, axis=0)
    return normalised_df


def remove_spectral_regions(dataframe):
    """Data at certain wavelengths unusable due to water spectrum: this function removes those specific sections"""
    low_range = dataframe[dataframe.index < 1890]
    high_range = dataframe[(1990 < dataframe.index)]
    high_range = high_range[high_range.index < 2400]
    modified_df = pd.concat([low_range, high_range], sort=True)
    return modified_df

def calculate_variable_regions(variance_dataframe):
    variances = variance_dataframe
    modified_df = remove_spectral_regions(variances)
    collection = {}
    for num in range(len(modified_df.columns)):
        series = modified_df.iloc[:, num].copy()
        average = series.mean()
        name = modified_df.columns[num]
        std_dev = series.std()
        confidence_interval = (average-(2*std_dev), average+(2*std_dev))
        series_mod = series.where((series < confidence_interval[0])|(series > confidence_interval[1]))
        series_mod.dropna(inplace=True)
        collection[name] = {"Average": average, 'St_dev': std_dev, "Confidence":confidence_interval,
                            "Variable Wavelegnths": series_mod.index.values}
    df_output = pd.DataFrame.from_dict(collection)
    return df_output


def main():
    """Runs the full process of analysis"""
    df_NIR = nir_data_to_dataframe()
    variance_df = calculate_variance(df_NIR)
    averaged_df = average_df_columns(df_NIR)
    diluent_series,  drug_only_avg_df = remove_diluent_values(averaged_df, "Saline")
    distance_df = calculate_distance_from_diluent(drug_only_avg_df, diluent_series)
    normalised = normalise_data(distance_df, diluent_series)
    modified_normalised_averaged = remove_spectral_regions(normalised)
    ## calculate sample variance regions
    # calculate_variable_regions(variance_df)
    ## calculate distance_variance regions
    variable_sites = calculate_variable_regions(modified_normalised_averaged)
    plot_full_spectra(df_NIR, "Full Spectrum NIR data")
    plot_full_spectra(variance_df, "Sample replicate variance", legend_state=True)
    distance_df.plot(title="Distance Diluent to Drug")
    # normalised.plot()
    modified_normalised_averaged.plot(title = "Distance diluent to Drug normalised by Diluent")
    plt.show()
    print(f" Variable regions : {variable_sites.to_string()}")
    return distance_df, variance_df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())
