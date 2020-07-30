import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.linear_model import LinearRegression
from file_IO import file_in, dataframe_to_csv
from PyQt5.QtWidgets import QApplication
import sys


def file_to_csv():
    filepath = file_in()[0]
    df = pd.read_csv(filepath, index_col=0)
    return df

def linearity(dataframe, x_axis):
    shape = dataframe.shape
    n_rows = shape[0]
    linearity_dict = {}
    for num in range(n_rows):
        laser = dataframe.index.values[num]
        y_axis = np.array(dataframe.iloc[num, :]).reshape(-1, 1)
        x_axis = np.array(x_axis).reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(x_axis, y_axis)
        intercept = reg.intercept_
        coefficient = reg.coef_
        score = reg.score(x_axis, y_axis)
        linearity_dict[laser] = (coefficient[0][0], intercept[0], score)
    linearity_df = pd.DataFrame.from_dict(linearity_dict, orient='index')
    linearity_df.columns = ["Coefficient", "Intercept", "R squared"]
    return linearity_df

def check_df_shape(df1, df2):
    shape1a, shape1b = df1.shape
    shape2a, shape2b = df2.shape
    if (shape1a == shape2a)and(shape1b == shape2b):
        return True
    elif shape1b == shape2b:
        return True
    else:
        return False


def compare_two_linearity(df1, df2):
    laser_list = ["Laser1", "Laser2", "Laser4", "Laser5", "Laser6", "Laser7", "Laser8"]
    checker =  check_df_shape(df1, df2)
    if checker == True:
        linear_dict = {}
        for num in range(df1.shape[0]):
            row_df1 = df1.iloc[num, :]
            row_df2 = df2.iloc[num, :]
            row_df1 = np.array(row_df1).reshape(-1, 1)
            row_df2 = np.array(row_df2).reshape(-1, 1)
            reg = LinearRegression()
            reg.fit(row_df1, row_df2)
            coefficient = reg.coef_[0][0]
            intercept = reg.intercept_[0]
            score = reg.score(row_df1, row_df2)
            laser_string = str((laser_list[num]))
            linear_dict[laser_string] = (coefficient, intercept, score)
    else:
        raise Exception("Incorrect DataFrame Shape. DataFrames must have same number of columns")
    compare_df = pd.DataFrame.from_dict(linear_dict)
    compare_df.index = ["Coefficient", "Intercept", "R Squared"]
    return compare_df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    df1 = file_to_csv()
    df2 = file_to_csv()
    print(df1.to_string())
    print(df2.to_string())

    linearity_compare_df = compare_two_linearity(df1, df2)
    dataframe_to_csv(linearity_compare_df)

    # regression = linearity(df1, [5, 20, 35, 50, 60])
    # print(regression.to_string())
    # dataframe_to_csv(regression)
    sys.exit(app.exec_())
    