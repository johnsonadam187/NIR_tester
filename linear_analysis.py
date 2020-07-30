import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

"""Reshapes data into correct format, fits the linear model and returns unpacked values for coefficient
 intercept and r squared for linear regression"""

def linear_analysis(x_data, y_data):
    x_axis = np.array(x_data).reshape(-1, 1)
    y_axis = np.array(y_data).reshape(-1, 1)
    reg = LinearRegression()
    if len(x_axis) == len(y_axis):
        reg.fit(x_axis, y_axis)
        coefficient = reg.coef_[0][0]
        intercept = reg.intercept_[0]
        r_squared = reg.score(x_axis, y_axis)
        return coefficient, intercept, r_squared
    else:
        raise Exception("Incorrect data format. Check shape of data Series")


if __name__ == "__main__":
    x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    y_axis = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    m, c, r2 = linear_analysis(x_axis, y_axis)
    print(r2, m, c)