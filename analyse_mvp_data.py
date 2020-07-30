import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from file_IO import file_in, file_path_to_df, dataframe_save_to_csv
import sys
from PyQt5.QtWidgets import QApplication
from linear_analysis import linear_analysis
"""Full analysis from importing df of Veriphi MVP data"""


def file_to_dataframe():
    file_path = file_in()
    df = pd.read_csv(file_path, index_col=0)
    df.drop(columns = ["CONCENTRATION"], inplace=True)
    df.index = ["Laser 1", "Laser 2", "Laser 3", "Laser 4", "Laser 5", "Laser 6", "Laser 7", "Laser 8"]
    df.drop(["Laser 3"], inplace=True)
    return df


def remove_diluent_col(dataframe, diluent_string):
    filter_mask = dataframe.columns.str.contains(diluent_string)
    anti_filter = [not item for item in filter_mask]
    new_df = dataframe[dataframe.columns[anti_filter]]
    diluent_var = dataframe[dataframe.columns[filter_mask]].var(axis=1)
    diluent_avg = dataframe[dataframe.columns[filter_mask]].mean(axis=1)
    return new_df, diluent_var, diluent_avg


def calculate_variance(dataframe):
    col_name_list = [item[:2] for item in dataframe.columns]
    unique_list = np.unique(col_name_list)
    collection = {}
    for item in unique_list:
        filter_mask = dataframe.columns.str.contains(item)
        new_df = dataframe[dataframe.columns[filter_mask]]
        variance = new_df.var(axis=1)
        collection[item] = variance
    variance_df = pd.DataFrame.from_dict(collection)
    return variance_df


def average_cols(dataframe):
    col_name_list = [item[:2] for item in dataframe.columns]
    unique_list = np.unique(col_name_list)
    collection = {}
    for item in unique_list:
        filter_mask = dataframe.columns.str.contains(item)
        series_name = item
        series = dataframe[dataframe.columns[filter_mask]].mean(axis=1)
        collection[series_name] = series
    average_df = pd.DataFrame.from_dict(collection)
    return average_df


def linearity(dataframe):
    collection = {}
    x_axis = [float(item) for item in dataframe.columns]
    for index, item in enumerate(dataframe.index):
        y_axis = dataframe.iloc[index, :]
        m, c, r2 = linear_analysis(x_axis, y_axis)
        collection[item] = (m, c, r2)
    linearity_df = pd.DataFrame.from_dict(collection)
    return linearity_df


def main():
    df1 = file_to_dataframe()
    variance = calculate_variance(df1)
    df_drugs_only, diluent_variance, diluent_avg = remove_diluent_col(df1, "9.0")
    average_df = average_cols(df_drugs_only)
    linear_df = linearity(average_df)
    return linear_df, variance, average_df, diluent_variance, diluent_avg


if __name__ == "__main__":
    app = QApplication(sys.argv)
    linearity, variance, average, diluent_var, diluent_avg = main()
    print(linearity.to_string())
    print(variance)
    # dataframe_save_to_csv(linearity)
    # dataframe_save_to_csv(variance)
    sys.exit(app.exec_())