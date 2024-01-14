"""
Created by: Hier Ihre Namen und Matrikelnummern


Hier die Antworten zu den Theoriefragen:
...

"""
import sys
import pathlib
import threading
import requests
import time
from threading import Event

PYQTV = None

try:
    from PyQt5 import QtWidgets, uic
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtGui import QPixmap, QImage

    PYQTV = 5

except ModuleNotFoundError:
    from PyQt6 import QtWidgets, uic
    from PyQt6.QtWidgets import QMessageBox
    from PyQt6.QtGui import QPixmap, QImage

    PYQTV = 6

import appprojekt2.filehandling as files
from appprojekt2.fileDialog import FileDialog
from appprojekt2.popUpWindow import show_message


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # main window attributes
        self.data = None
        self.file_handler = files.FileHandler()
        self.file_dialog = FileDialog()

        # get current working directory
        working_dir = str(pathlib.Path(__file__).parent.resolve())

        # load the GUI file from QtDesigner
        self.main_window = uic.loadUi(working_dir + '/resources/window.ui', self)

        # TODO: lösung
        # legen Sie ein Event an, dass es ermöglicht den Stream der Corona Fallzahlen zu starten und zu stoppen
        self.corona_data_event = threading.Event()
        # implementieren Sie einen Thread, weisen Sie ihm die Methode self.stream_corona_data zu
        # und das Event als parameter
        thread = threading.Thread(target=self.stream_corona_data, args=(self.corona_data_event,))
        # starten Sie den Thread
        thread.start()

        # call the UI handler
        self.button_handler()
        # display the GUI
        self.show()

    def button_handler(self):
        """
        Handles all the UI button callbacks
        means: which function is called for which button press.
        """
        self.main_window.btnOpenFile.clicked.connect(self.open_data)
        self.main_window.btnPlotData.clicked.connect(self.visualize_data)
        self.main_window.btnExportFile.clicked.connect(self.export_data)
        self.main_window.btnShowStats.clicked.connect(self.show_statistics)
        self.main_window.btnClearAll.clicked.connect(self.clear_all)
        self.main_window.btnDeleteColumns.clicked.connect(self.main_window.tableDataset.delete_columns)
        self.main_window.btnShowCorrelations.clicked.connect(self.show_correlation_matrix)
        # TODO: lösung
        # Beim Drücken der Buttons soll etwas mit dem Event gemacht werden
        self.main_window.btnStartCoronaStream.clicked.connect(self.corona_data_event)
        self.main_window.btnStopCoronaStream.clicked.connect(self.corona_data_event)

    def open_data(self):
        """
        Wrapper for the open data method in file handler.
        """
        # call the file open dialog to select a file
        file_name = self.file_dialog.open_file_name_dialog()

        # check first if a file was selected
        if file_name is None:
            show_message('Please select a file!')
            # return bricht methode ab, daher kein else notwendig
            return None

        # open the file and save the data to self.data
        self.data = self.file_handler.open_file(file_name)

        # put that data into the table widget
        self.main_window.tableDataset.display_data(self.data)

    def export_data(self):
        """
        Wrapper for the save file method in FileHandler. Takes the file path and
        adds "_modified" to the filename and saves the DataFrame object to this .csv.
        """
        # check if a file was opened before
        if self.data is None:
            show_message('Please open first a file before exporting one!')
            return None

        # call the save file dialog to select a file name and destination
        file_path_export = self.file_dialog.save_file_dialog()

        # check if a file was selected, if not return and do not try to save the file
        if file_path_export is None:
            return None

        # update the data in filehandler. This is necessary when we delete columns
        self.file_handler.data = self.main_window.tableDataset.df
        # call the save file method from FileHandler
        self.file_handler.save_file(file_path_export)

    def visualize_data(self):
        """
        Call the open_data() method and creates a plot.
        """
        # check if a file was opened before
        if self.data is None:
            show_message('Please open first a file before plotting!')
            return None

        self.data = self.data.dropna()

        # check which columns were clicked by the user
        selected_columns = self.main_window.tableDataset.get_selected_columns()
        # we need at least two selected columns to plot something
        if len(selected_columns) < 2:
            show_message('Please select at least two columns!')
            return None

        # x is the first selected column
        x = self.data.iloc[:, selected_columns[0]]
        # y the second
        y = self.data.iloc[:, selected_columns[1]]

        # the labels are the names of the selected columns
        # to get the names, we take the index of the selected column: selected_columns[0]
        # then we take all the column names of our data: self.data.columns
        # and combine both to get the right names:
        x_label = self.data.columns[selected_columns[0]]
        y_label = self.data.columns[selected_columns[1]]
        # call the plot function of our own plotting class

        # check which kind of plot is selected
        if self.main_window.rbScatter.isChecked():
            self.main_window.plotDataset.scatter_plot(x, y, x_label, y_label, title='Interesting')

        else:
            self.main_window.plotDataset.line_plot(x, y, x_label, y_label, title='Interesting')

    def show_statistics(self):
        """
        Calculates the statistic values of the loaded data set and plots them
        to another table.
        """
        # check if a file was opened before
        if self.data is None:
            show_message('Please open first a file before plotting statistics!')
            return None

        # get the statistic values
        stats = self.data.describe()
        # use the display data method of our class tableWidget to show the statistics
        self.main_window.tableStatistics.display_data(stats)

        # finally set the row labels to the table (mean, std, etc..)
        self.main_window.tableStatistics.setVerticalHeaderLabels(stats.axes[0])

    def show_correlation_matrix(self):
        """
        Computes the correlation matrix for a DataFrame object
        and displays it in a custom tableWidget.
        """
        # first create the sub data set
        # we can do this the same way we did it in exercise 1
        # or, we use our delete columns method and create a new data set
        happiness_data = self.data[['Happiness Score',
                                    'Economy (GDP per Capita)', 'Family',
                                    'Health (Life Expectancy)', 'Freedom', 'Trust (Government Corruption)',
                                    'Generosity', 'Dystopia Residual']]

        # compute the correlation matrix
        corr = happiness_data.corr(method='pearson')
        # set the matrix to the tablewidget (round to one decimal)
        self.main_window.tableCorrelations.display_data(corr.round(1))
        # set also the vertical names of the matrix
        self.main_window.tableCorrelations.setVerticalHeaderLabels(corr.columns)

    def clear_all(self):
        """
        Clears the UI tables and the graph
        """
        # first, we clear the variables aka the data, then the UI!
        self.data = None

        # clearing the tables
        self.main_window.tableDataset.clear()
        self.main_window.tableStatistics.clear()
        self.main_window.tableCorrelations.clear()
        # clearing the plot window
        self.main_window.plotDataset.clear()

    def closeEvent(self, event):
        """
        Window that pops up when the red x in the corner is clicked.
        """
        reply = QMessageBox.question(self, 'Message',
                                     'Sind Sie sicher, dass Sie beenden möchten?',
                                     QMessageBox.Yes | QMessageBox.No)
        self.when_closing(reply, event)

    def when_closing(self, reply, event):
        """
        Is called when the app is closed.
        """
        if reply == QMessageBox.Yes:
            print('App is closed now')
            event.accept()
            # TODO: lösung
            # hier etwas mit dem Event machen, sodass die API Anfrage gestoppt wird
            event.clear()

        else:
            print('Changed my mind')
            event.ignore()

    def start_event(self):
        self.corona_data_event.set()

    def stop_event(self):
        self.corona_data_event.clear()

    def stream_corona_data(self, e_start_stream: Event):
        """
        Uses an API call to receive corona data from RKI.
        """
        # TODO: lösung
        # variablen initialisieren
        # wir brauchen zwei Listen, eine für die x-Achse und eine für die y_Achse
        x = []
        y = []
        days_counter = 1

        while True:
            if not e_start_stream.is_set():
                time.sleep(1) # bitte nicht entfernen
                # variablen zurücksetzen (nur wenn Sie wollen, dass der Stream jedes Mal von Vorne anfängt)
                x = []
                y = []
                days_counter = 1
                break
            else:
                time.sleep(1) # bitte nicht entfernen

                # das ist die URL für den API Call. Wir hängen hinten die Anzahl an Tagen an, wie weit zurück wir
                # die Fallzahlen ausgegeben haben wollen
                base_url = "https://api.corona-zahlen.org/germany/history/cases/"+str(days_counter)

                try:
                    # api call
                    data = requests.get(base_url).json()

                except requests.exceptions.JSONDecodeError:
                    print('Error pulling data')

                else:
                    # print(data['data'][0])
                    # append Daten an die Liste für die x-Achse (eigentlich nur die Anzahl an vergangenen Tagen)
                    for i in range(days_counter):
                        x.append(i+1)
                    # append Daten an die Liste für die y-Achse. Hier brauchen wir die Fallzahlen.
                    # Diese müssen wir aus der response des API calls "ausschneiden"
                    for corona_data in data['data']:
                        y.append(corona_data['cases'])

                    # abfragen, ob scatter oder line plot
                    if self.main_window.rbScatter.isChecked():
                        # scatter plot Liste x-Achse über Liste y-Achse
                        self.main_window.plotDataset.scatter_plot(x, y, 'Vergangene Tage', 'Corona Fälle',
                                                                  'Corona Fälle in Deutschland')
                    else:
                        # line plot
                        self.main_window.plotDataset.line_plot(x, y, 'Vergangene Tage', 'Corona Fälle',
                                                               'Corona Fälle in Deutschland')
                    # vergangene Tage inkrementieren (erhöhnen um eins)
                    days_counter += 1


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setWindowTitle('App Projekt 2')

    if PYQTV == 5:
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())
