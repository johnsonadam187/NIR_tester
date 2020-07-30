import pandas as pd
import numpy as np
import seaborn as sns
from file_IO import file_in, file_path_to_df, dataframe_save_to_csv
from PyQt5.QtWidgets import QApplication
from analyse_mvp_data import average_cols, linearity
import matplotlib.pyplot as plt
import sys
from linear_analysis import linear_analysis


def file_to_df():
    df = file_path_to_df(file_in())
    df.drop(columns = ["CONCENTRATION"], inplace = True)
    df.index = ["Laser 1", "Laser 2", "Laser 3", "Laser 4", "Laser 5", "Laser 6", "Laser 7", "Laser 8", "Temperature"]
    df.drop(['Laser 3'], inplace = True)
    return df


def normalise_over_temp(dataframe):
    temp_series = dataframe.loc["Temperature"]
    dataframe.drop(["Temperature"], inplace=True)
    collection = {}
    for num in range(len(dataframe.columns)):
        name = dataframe.columns[num]
        series = dataframe.iloc[:, num]
        normalise = series/temp_series[num]
        collection[name] = normalise
    normalised_df = pd.DataFrame.from_dict(collection)
    return normalised_df


def average_columns_for_concentration(dataframe):
    avg_df = average_cols(dataframe)
    return avg_df


def calculate_distance_to_diluent(dataframe, diluent_string, rename_string):
    diluent_series = dataframe.loc[:, diluent_string]
    diluent_series.name = rename_string
    dataframe.drop(columns = [diluent_string], inplace=True)
    distance_df = dataframe.subtract(diluent_series, axis=0)
    return distance_df


def plot_lasers_subplots(dataframe, num_subplot_columns, axis=1):
    """plots MVP data for lasers, data format exported from raw data interface, custom export"""
    if axis == 0:
        n_series = len(dataframe.index)
        n_sub_cols = num_subplot_columns
        if n_series % n_sub_cols != 0:
            sub_rows = int(n_series/n_sub_cols)+1
            sub_cols = n_sub_cols
            fig1, axs = plt.subplots(sub_rows, sub_cols, figsize=(15, 15))
            axs[-1, -1].axis('off')
            counter = 0
            counter_limit = len(dataframe.index)
            for i in range(sub_rows):
                for j in range(sub_cols):
                    # axs[i, j].scatter(dataframe.iloc[counter, :], [float(item) for item in dataframe.columns])
                    x_axis = dataframe.iloc[counter,:]
                    y_axis = [float(item) for item in dataframe.columns]
                    p1 = sns.regplot(x_axis, y_axis, scatter=True, fit_reg=True, ax=axs[i, j], line_kws={'color': 'red'})
                    regr = linear_analysis(x_axis, y_axis)
                    anno_string = f"y = {regr[0]:.5f}x + {regr[1]:.5f} (r2 = {regr[2]:.5f})"
                    axs[i, j].annotate(anno_string, xy=(1, 2))
                    p1.text(x_axis[2], y_axis[2], anno_string, horizontalalignment= 'right', verticalalignment="top")
                    # axs[i, j].title.set_text(dataframe.index[counter])
                    plt.setp(axs[i, j].xaxis.get_majorticklabels(), rotation=20)
                    counter += 1
                    if counter == counter_limit:
                        break
            # plt.tight_layout()
            plt.subplots_adjust(hspace=0.91)
            plt.show()


def main():
    df1 = file_to_df()
    df2 = normalise_over_temp(df1)
    df3 = average_columns_for_concentration(df2)
    df4 = calculate_distance_to_diluent(df3, "9.", "Saline")
    df5 = linearity(df4)
    # print(df3)
    plot_lasers_subplots(df3, 2, axis=0)

    # plt.scatter([float(item) for item in df3.columns], df3.loc["Laser 2"])
    # plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())