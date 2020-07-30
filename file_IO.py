from PyQt5.QtWidgets import QFileDialog, QApplication
import sys
import pandas as pd


def file_in():
    """opens file dialog to pick csv, returns filepath"""
    dialog = QFileDialog()
    file_path_list = dialog.getOpenFileNames(filter="*.csv")
    return file_path_list[0][0]


def file_path_to_df(filepath, index_col=0):
    df1 = pd.read_csv(filepath, index_col=index_col)
    return df1


def dataframe_save_to_csv(dataframe):
    dialog = QFileDialog()
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    file_path = dialog.getSaveFileName()
    dataframe.to_csv(f"{file_path[0]}.csv")

def convert_txt_to_csv():
    dialog = QFileDialog()
    file_path = dialog.getOpenFileName()[0]
    df1 = pd.read_csv(file_path)
    return df1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    df1 = convert_txt_to_csv()
    print(df1)
    sys.exit(app.exec_())
