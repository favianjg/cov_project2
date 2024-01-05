try:
    from PyQt5 import QtWidgets, QtCore
except ModuleNotFoundError:
    from PyQt6 import QtWidgets, QtCore


def show_message(msg: str):
    """
    Opens a dialog with a custom message.
    Useful for error or warning messages.
    """
    # print the message also to the console
    # remember, this is not visible in a distributed app!
    print(msg)

    main_window = QtCore.QCoreApplication.instance().activeWindow()

    # open dialog and show message
    error_dialog = QtWidgets.QErrorMessage(main_window)
    error_dialog.showMessage(msg)
    error_dialog.show()
