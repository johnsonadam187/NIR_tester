import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication
from file_IO import file_in, file_path_to_df, dataframe_save_to_csv
import sys
import seaborn as sns
from analyse_nir_data import main as nir_data_process
from Linear_process_for_raw_NIR_data import reduce_to_MVP_wavelengths
import matplotlib.pyplot as plt
from linear_analysis import linear_analysis


def sub_plot_for_nir(dataframe):
    num_rows = 4
    num_cols = 2
    fig1, axs = plt.subplots(nrows = num_rows, ncols = num_cols, figsize=(15, 15))
    axs[-1, -1].axis('off')
    counter = 0
    for i in range(num_rows):
        for j in range(num_cols):
            series_x = [20, 35, 50, 5, 60]
            series_y = dataframe.iloc[:, counter]
            p1 = sns.regplot(series_x, series_y, scatter=True, fit_reg=True, ax=axs[i, j], line_kws={'color': 'red'})
            regr = linear_analysis(series_x, series_y)
            anno_string = f"y = {regr[0]:.5f}x + {regr[1]:.5f} (r2 = {regr[2]:.5f})"
            axs[i, j].annotate(anno_string, xy=(1, 2))
            p1.text(series_x[2], series_y [2], anno_string, horizontalalignment='right', verticalalignment="top")
            # axs[i, j].title.set_text(dataframe.index[counter])
            plt.setp(axs[i, j].xaxis.get_majorticklabels(), rotation=20)
            counter += 1
            if counter >= len(dataframe.columns):
                break
    plt.subplots_adjust(hspace=0.91)
    fig1.suptitle("NIR Linearity vs Concentration at MVP wavelengths")
    plt.show()


def nir_analysis():
    distance_drug_to_diluent, variance_df = nir_data_process()
    nir_at_mvp, var_at_mvp = reduce_to_MVP_wavelengths(distance_drug_to_diluent,  variance_df,
                                                       [1310, 1387, 1550, 1654, 1670, 1749, 1850])
    print(distance_drug_to_diluent.to_string())
    print("NIR Data at MVP wavelength 'nir_at_mvp'")
    print(nir_at_mvp.to_string())
    print("Replicate variance NIR at MVP wavelengths 'var_at_mvp'")
    print(var_at_mvp.to_string())

    sub_plot_for_nir(nir_at_mvp)
    # for num in range(len())




def main():
    nir_analysis()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())