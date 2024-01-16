import sys
import requests
from PyQt5 import QtWidgets, QtCore
import json
import urllib3
import time
import pyqtspinner

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QVBoxLayout, QDesktopWidget)
from pyqtspinner.spinner import WaitingSpinner
from home import HomeScreen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel


class WarningDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")

        self.label = QLabel(message)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Close the dialog when clicked

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(ok_button)
        screen = QDesktopWidget().availableGeometry()

        self.setGeometry(int((screen.width() - self.width()) / 2),
                         int((screen.height() - self.height()) / 2), 200, 50)
        self.setLayout(layout)


class APICaller(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)  # Signal to emit data when finished

    def __init__(self, parent=None):
        super().__init__(parent)

    def make_api_call(self, url, method="GET", body=None):
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request(method, url, headers=headers, data=json.dumps(body))

            response.raise_for_status()  # Raise an exception for non-200 status codes

            self.finished.emit(response.json())  # Emit JSON response data


        except requests.exceptions.RequestException as e:
            warning_dialog = WarningDialog("Login Failed!!")
            warning_dialog.exec_()
            print("API call error:", e)
            self.finished.emit(None)  # Emit None on error


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.resize(500, 120)
        self.api_caller = APICaller()
        self.api_caller.finished.connect(self.handle_api_response)
        self.spinner = WaitingSpinner(self)  # Create WaitingSpinner instance
        # self.spinner.start_spinning()
        layout = QGridLayout()

        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton('Login')
        # button_login.clicked.connect(self.check_password)

        button_login.clicked.connect(lambda: [self.spinner.start(), self.check_password()])

        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)
        self.home = HomeScreen()
        # layout.addWidget(self.home)

        self.spinner = WaitingSpinner(self)  # Create WaitingSpinner instance
        layout.addWidget(self.spinner)
        self.setLayout(layout)

    def check_password(self):
        msg = QMessageBox()
        self.make_api_request(self.lineEdit_username.text(), self.lineEdit_password.text())
        self.api_caller.finished.connect(self.handle_api_response)

    # if self.lineEdit_username.text() == 'Usernmae' and self.lineEdit_password.text() == '000':
    # 	msg.setText('Success')
    # 	msg.exec_()
    # 	app.quit()
    # else:
    # 	msg.setText('Incorrect Password')
    # 	msg.exec_()

    def make_api_request(self, userName, password):
        url = "http://localhost:3000/user/login"
        # self.spinner.start()
        self.api_caller.make_api_call(url, "POST", {"userName": userName, "password": password})

    def handle_api_response(self, response_data):
        if response_data is not None:
            # Process the received API data here
            # self.show_warning_messagebox()
            if not response_data["success"]:
                # self.spinner.stop()
                self.show_warning_messagebox()
            elif response_data["success"]:
                # home.open_home()
                form.hide()
                self.home.show()
            # print(response_data)
        else:
            self.show_warning_messagebox()
            print("API call failed")

    def show_warning_messagebox(self):
        print("warning message clicked")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        # setting message for Message Box
        msg.setText("Warning")

        # setting Message box window title
        msg.setWindowTitle("Warning MessageBox")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # start the app
        retval = msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec_())
