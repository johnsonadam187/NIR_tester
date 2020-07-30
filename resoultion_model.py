import pandas as pd
import numpy as np
import sklearn
from analyse_mvp_data import main as mvp_linearity_and_var
from PyQt5.QtWidgets import QApplication
import sys


def import_mvp_linearity_and_variance():
    linearity_df, variance, average_df, diluent_variance, diluent_mean = mvp_linearity_and_var()
    return linearity_df, variance, average_df, diluent_variance, diluent_mean


def assess_variance(variance_dataframe):
    collection = {}
    for index, item in enumerate(variance_dataframe.index):
        name = item
        average = variance_dataframe.iloc[index, :].mean()
        collection[name] = average
    return collection


def main():
    drug_linearity, drug_variance, drug_average, diluent_variance, diluent_average = import_mvp_linearity_and_variance()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())