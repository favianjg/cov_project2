"""
My first application
Author: Luis Garcia
Facility: ZOT
University: Aalen University
"""
import pandas as pd
from appprojekt2.popUpWindow import show_message


class FileHandler:
    def __init__(self):
        self.data = None
        self.file_path = None

    def open_file(self, file_path: str):
        """
        Opens a .csv file and read the data.
        """
        # try to open the file at file_path (path and file name in one string)
        try:
            self.data = pd.read_csv(file_path, on_bad_lines='skip', encoding='unicode_escape')
            return self.data

        # if the file does not exist, this exception is called
        except FileNotFoundError:
            # and this error message is printed
            show_message('No File: %s' % file_path)
            return None

        # if successful save the file path to the class attribute for later use
        finally:
            # copy file path to class attribute
            self.file_path = file_path
            return self.data

    def save_file(self, file_path: str):
        """
        Saves the data from the before opened .csv file
        to a new .csv file.
        """
        # check if the file_path is empty
        if file_path == '':
            # print an error message if so, and return - do not try to save the file, won't work!
            print('No file path was given when tried to save the data to .csv!')
            return

        # check if data was opened before (only then it can be saved again)
        if self.data is not None:
            self.data.to_csv(path_or_buf=file_path, sep=',', index=False)

        else:
            print('No .csv file was opened before!')
