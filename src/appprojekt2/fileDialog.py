try:
    from PyQt5.QtWidgets import QWidget, QFileDialog
except ModuleNotFoundError:
    from PyQt6.QtWidgets import QWidget, QFileDialog


class FileDialog(QWidget):

    def __init__(self):
        super().__init__()

    def open_file_name_dialog(self):
        """
        Open a dialog window to select a file.
        """
        options = QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "csv Files (*.csv);;All Files (*)", options=options)
        if file_name:
            return file_name

    def open_file_names_dialog(self):
        """
        Open a dialog window to select multiple files.
        """
        options = QFileDialog.Option.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "csv Files (*.csv);;All Files (*)", options=options)
        if files:
            return files

    def save_file_dialog(self):
        """
        Open a dialog window to save data to a file.
        """
        options = QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "csv Files (*.csv);;All Files (*)", options=options)
        if file_name:
            return file_name
