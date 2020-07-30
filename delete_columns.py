import pandas as pd
from file_IO import file_in, file_path_to_df, dataframe_save_to_csv
from PyQt5.QtWidgets import QApplication
import sys


def delete_columns():
    file_path = file_in()
    df1 = file_path_to_df(file_path)
    loop = True
    while loop == True:
        print(f"Dataframe columns {[item for item in df1.columns]}")
        col_name = input("List substance to remove from dataframe : ")
        df1 = df1.iloc[:, ~df1.columns.str.contains(col_name)].copy()
        print(f"Dataframe columns {[item for item in df1.columns]}")
        breaker = input("Save Dataframe type 'S' or delete more columns type 'D' : ").lower()
        if breaker == "s":
            dataframe_save_to_csv(df1)
            loop = False
        elif breaker == "d":
            continue
        else:
            raise Exception("Incorrect entry try again")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    delete_columns()
    sys.exit(app.exec_())