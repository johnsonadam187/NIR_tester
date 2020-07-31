import pandas as pd
from file_IO import file_in, file_path_to_df, dataframe_save_to_csv
from PyQt5.QtWidgets import QApplication
import sys

def main():
    path = file_in()
    df1 = file_path_to_df(path)
    loop = True
    while loop == True:
        col_list = list(df1.columns)
        print(col_list)
        initial_string = input("Which columns to change? ")
        new_string = input("Enter Replace String : ")
        new_col_list = [item.replace(item, new_string) if initial_string in item else item for item in col_list]
        print(new_col_list)
        df1.columns = new_col_list
        save_spec = input("Enter 'S' to save dataframe or 'C' to change more columns").lower()
        if save_spec == "s":
            dataframe_save_to_csv(df1)
            loop = False
        elif save_spec == 'c':
            continue
        else:
            raise Exception("Incorrect entry. Try again")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())