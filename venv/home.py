import sys
import requests
from PyQt5 import QtWidgets, QtCore
import json
import urllib3
import time
import pyqtspinner

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QVBoxLayout, QDesktopWidget)
# from pyqtspinner.spinner import WaitingSpinners
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel
from add_new_record import AddRecordScreen


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        # app = QApplication(sys.argv)
        self.setWindowTitle("Home Screen")
        self.resize(500, 120)
        # self.spinner = WaitingSpinner(self)  # Create WaitingSpinner instance
        # self.spinner.start_spinning()
        layout = QGridLayout()

        button_new_reord = QPushButton('Add new record')
        # button_new_reord.clicked.connect(lambda: [self.spinner.start(), self.add_new_record()])
        button_new_reord.clicked.connect(self.add_new_record)

        layout.addWidget(button_new_reord, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)
        self.addrecord = AddRecordScreen()
        # self.spinner = WaitingSpinner(self)  # Create WaitingSpinner instance
        # layout.addWidget(self.spinner)
        self.setLayout(layout)
        # sys.exit(app.exec_())
    def add_new_record(self):
        self.hide()
        self.addrecord.show()
        print("button clicked")
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     home = HomeScreen()
#     home.show()
#     sys.exit(app.exec_())
