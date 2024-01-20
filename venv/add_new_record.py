import sys
import os
import requests
from PyQt5 import QtWidgets, QtCore
import json
import urllib3
import time
import pyqtspinner

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QVBoxLayout, QDesktopWidget,  QPushButton, QFileDialog)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel
# from add_new_record_helper import *

from PyQt5.QtCore import QTimer, Qt
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
import math
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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



class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)  # Create a QTimer instance
        self.timer.timeout.connect(self.update_timer)  # Connect timeout signal to update method
        self.time_elapsed = 0

        self.timer_label = QLabel("00:00:00", self)  # Create label to display timer

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        self.setLayout(layout)

    def start_timer(self):
        self.timer.start(1000)  # Emit timeout signal every 1000 milliseconds (1 second)

    def update_timer(self):
        self.time_elapsed += 1
        hours = self.time_elapsed // 3600
        minutes = (self.time_elapsed % 3600) // 60
        seconds = self.time_elapsed % 60
        time_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"  # Format time string
        self.timer_label.setText(time_text)

    def stop_timer(self):
        self.timer.stop()



class AddRecordScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.resize(500, 120)
        self.timer = TimerWidget()
        self.selectExcelButton = QPushButton("Select Excel File")
        self.selectExcelButton.clicked.connect(self.open_file)  # Connect to a function for file selection

        self.pdffilename = ""
        self.selectpdfbutton = QPushButton("Select Blank pdf File")
        self.selectpdfbutton.clicked.connect(self.open_pdf_file)
        self.selectpdfbutton.setDisabled(True)

        self.driver = ""
        self.fileName = ""

        self.openBrowserButton = QPushButton("Open browser")
        self.openBrowserButton.setDisabled(True)
        self.openBrowserButton.clicked.connect(lambda: [self.openBrowser(),self.openBrowserButton.setDisabled(True), ])

        # self.postLoginButton = QPushButton("Click after successfully logged in")
        # self.postLoginButton.setDisabled(True)
        # self.postLoginButton.clicked.connect(lambda:[self.openBrowserButton.setDisable(True), openAddRecordPage])

        layout = QGridLayout()  # Or any other layout you're usingß
        layout.addWidget(self.selectExcelButton)
        layout.addWidget(self.selectpdfbutton)
        layout.addWidget(self.openBrowserButton)
        # layout.addWidget(self.timer)
        self.label_name = QLabel('<font size="4"> Please Login within 30sec after browser opened </font>')
        layout.addWidget(self.label_name)
        # layout.addWidget(self.postLoginButton)

        layout.setRowMinimumHeight(2, 75)
        self.setLayout(layout)

    def addRecordHelper(self,ind, lpmno, lpmext, base_survey_no, sd_no, land_nature_webland,total_ext, land_classification, land_nature_broad_cat, land_nature_sub_cat, land_nature_sub_cat_two, land_classification_broad_cat,land_classification_sub_cat,land_classification_sub_cat_two,land_usage, source_of_irrigation,katha_num, pattadhar_name, relation_name):
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="liselected"]/a').click()

        time.sleep(1)
        lpm_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtlpmno_0"]')
        lpm_input.clear()
        lpm_input.send_keys(str(lpmno))

        time.sleep(.10)
        lpm_ext_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtlpmnoExtent_0"]')
        lpm_ext_input.clear()
        lpm_ext_input.send_keys(str(lpmext))


        time.sleep(.10)
        base_survery_no_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtwebsysno_0"]')
        base_survery_no_input.clear()
        base_survery_no_input.send_keys(str(base_survey_no))


        time.sleep(.10)
        sd_no_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtwebsubno_0"]')
        sd_no_input.clear()
        sd_no_input.send_keys(str(sd_no))


        time.sleep(.10)
        total_ext_input = self.driver.find_element(By.XPATH, '// *[ @ id = "grAddRecord_txttotalextent_0"]')
        total_ext_input.clear()
        total_ext_input.send_keys(str(lpmext))

        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlBroadCategory_LandNature1_0"]/option[2]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlBroadCategory_LandNature1_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str(land_nature_broad_cat))
        except TimeoutException:
            print("Exception in filling land nature, broad cat!!")
        time.sleep(1)

        if str(land_nature_sub_cat) != str(float('nan')):
            try:
                element = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandNature1_0"]/option[2]'))
                )
                # print("Option loaded")
                dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandNature1_0"]')
                dd_sel = Select(dd)
                dd_sel.select_by_value(str(land_nature_sub_cat))
            except TimeoutException:
                print("Exception in filling land nature subcat!!")
            time.sleep(1)

        if str(land_nature_sub_cat_two) != str(float('nan')):
            try:
                element = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandNature1_SubA_0"]/option[2]'))
                )
                # print("Option loaded")
                dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandNature1_SubA_0"]')
                dd_sel = Select(dd)
                dd_sel.select_by_value(str(land_nature_sub_cat_two))
            except TimeoutException:
                print("Exception in filling land nature, subcat two!!")

        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlBroadCategory_LandCalssification1_0"]/option[3]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlBroadCategory_LandCalssification1_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_visible_text(str(land_classification_broad_cat))
        except TimeoutException:
            print("Exception in filling land classification broad cat!!")

        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandClassification1_0"]/option[2]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandClassification1_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str(land_classification_sub_cat))
        except TimeoutException:
            print("Exception in filling land classification subcat!!")

        time.sleep(1)

        if str(land_classification_sub_cat_two) != str(float('nan')):
            try:
                element = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="grAddRecord_ddlSubCategory_LandClassification1_SubA_0"]/option[3]'))
                )
                # print("Option loaded")
                dd = self.driver.find_element(By.XPATH,
                                              '//*[@id="grAddRecord_ddlSubCategory_LandClassification1_SubA_0"]')
                dd_sel = Select(dd)
                dd_sel.select_by_value(str(land_classification_sub_cat_two))
                print("Exception in filling land classification subcat two!!")
            except TimeoutException:
                pass

        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlnatureoflanduse_0"]/option[2]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlnatureoflanduse_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str(land_usage))
        except TimeoutException:
            print("Exception in Land usage!!")

        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlSourceOfIrrigiAdd_0"]/option[2]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlSourceOfIrrigiAdd_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str(source_of_irrigation))
        except TimeoutException:
            print("Exception in source of irrigation!!")

        time.sleep(1)
        katha_no_input = self.driver.find_element(By.XPATH, '// *[ @ id = "grAddRecord_txtkhatano_0"]')
        katha_no_input.clear()
        katha_no_input.send_keys(str(katha_num))


        self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_btnKhata_0"]').click()

        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlLandNature1_0"]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlLandNature1_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str(land_nature_webland))
        except TimeoutException:
            print("Exception in Land nature webland!!")
        time.sleep(1)

        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '// *[ @ id = "grAddRecord_ddlLandClassification1_0"] / option[3]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '// *[ @ id = "grAddRecord_ddlLandClassification1_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str(land_classification))
        except TimeoutException:
            print("Exception in filling land classification!!")
        time.sleep(1)

        # To Upload File//*[@id="grAddRecord_txtnotalno_0"]
        s = self.driver.find_element(By.XPATH, '//*[@id="filetahsil"]')

        s.send_keys(self.pdffilename)
        time.sleep(.20)
        total_ext_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txttotalextent_0"]')
        total_ext_input.clear()
        total_ext_input.send_keys(str(total_ext))


        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlactionreq_0"]/option[1]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlactionreq_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str("1"))
        except TimeoutException:
            print("Error in action required setting!!")

        pattadarName = self.driver.find_element(By.XPATH,
                                                '//*[@id="grAddRecord_txtpattdarname_0"]').get_attribute(
            "value")
        pattadarRelation = self.driver.find_element(By.XPATH,
                                                    '//*[@id="grAddRecord_txtpattadarFname_0"]').get_attribute(
            "value")
        time.sleep(2)

        if str(pattadarName) == str(float('nan')) and str(pattadarRelation) == str(float('nan')):
            owner_phone_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtEnjoyerFname_0"]')
            owner_phone_input.clear()
            owner_phone_input.send_keys(str(relation_name))

            time.sleep(.30)
            father_name_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtEnjoyerName_0"]')
            father_name_input.clear()
            father_name_input.send_keys(str(pattadhar_name))


            time.sleep(.30)
            owner_name_input_ = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtpattdarname_0"]')
            owner_name_input_.clear()
            owner_name_input_.send_keys(str(pattadhar_name))


            time.sleep(.30)
            owner_father_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtpattadarFname_0"]')
            owner_father_input.clear()
            owner_father_input.send_keys(str(relation_name))

        else:
            owner_name_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtEnjoyerName_0"]')
            owner_name_input.clear()
            owner_name_input.send_keys(str(pattadarName))

            onwer_father_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtEnjoyerFname_0"]')
            onwer_father_input.clear()
            onwer_father_input.send_keys(str(pattadarRelation))

        time.sleep(1)

        lpm_ext_input = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtEnjoyerExtent_0"]')
        lpm_ext_input.clear()
        lpm_ext_input.send_keys(str(lpmext))

        time.sleep(.5)
        lpm_ext_input_ = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_txtpattadarExtent_0"]')
        lpm_ext_input_.clear()
        lpm_ext_input_.send_keys(str(lpmext))
        time.sleep(1)

        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="grAddRecord_ddlrightsreq_0"]/option[2]'))
            )
            # print("Option loaded")
            dd = self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_ddlrightsreq_0"]')
            dd_sel = Select(dd)
            dd_sel.select_by_value(str("1"))
        except TimeoutException:
            print("Error in rights setting!!")

        time.sleep(1)

        self.driver.find_element(By.XPATH, '//*[@id="grAddRecord_rbllistcultivate_add_0_1_0"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="btnAdd"]').click()
        time.sleep(3)
        submitAlert = self.driver.switch_to.alert
        if submitAlert.text != "Please check all the details before Final Submission":
            submitAlert.accept()
            # self.df.at[ind, 'status'] = "Incomplete"
            return False
        elif submitAlert.text == "Please check all the details before Final Submission":
            submitAlert.accept()
            time.sleep(6)
            completedAlert = self.driver.switch_to.alert
            completedAlert.accept()
            # self.df.at[ind, 'status'] = "Completed"
            time.sleep(6)

            print(str(lpmno), " Completed")
            return True


    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Optional: Use Qt's dialog for more control
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")

        if file_name:

            self.selectExcelButton.setDisabled(True)
            self.selectpdfbutton.setEnabled(True)
            self.fileName = file_name
            print("Selected file:", self.fileName)
            # Process the selected Excel file here

    def open_pdf_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Optional: Use Qt's dialog for more control
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")

        if file_name:
            self.openBrowserButton.setEnabled(True)
            self.selectpdfbutton.setDisabled(True)
            self.pdffilename = file_name
            print("Selected blank file name file:", self.pdffilename)
            # Process the selected Excel file here


    def openBrowser(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://webland2.ap.gov.in/POLR6/loginpage.aspx")
        time.sleep(1)
        self.driver.maximize_window()
        self.driver.find_element(By.XPATH, '//*[@id="useID"]').send_keys(str('tah03mdgl'))
        self.driver.find_element(By.XPATH, '//*[@id="pqrabc"]').send_keys(str('MROmdgl09'))
        # //*[@id="ddlDist"]
        try:
            # print("Option loaded")
            districtSelect = self.driver.find_element(By.XPATH, '//*[@id="ddlDist"]')
            distSel = Select(districtSelect)
            distSel.select_by_value('16')
        except TimeoutException:
            print("Exception in district selection!!")
        # Enter capcha and submit the form
        time.sleep(20)
        # "https://webland2.ap.gov.in/POLR6/loginpage.aspx"
        self.openAddRecordPage()

    def openAddRecordPage(self):
        self.driver.get("https://webland2.ap.gov.in/POLR6/NewProcess/DraftLandRegister.aspx")
        # "https://webland2.ap.gov.in/POLR6/NewProcess/DraftLandRegister.aspx"
        self.selectVillage()

    def selectVillage(self):
        time.sleep(1)
        dddlvillage = self.driver.find_element(By.XPATH, '//*[@id="ddlvillage"]')
        select_object = Select(dddlvillage)
        select_object.select_by_value('1623024')#1623024 for vommali, 1623004 for koormanatha puram
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="btngetdetails"]').click()
        time.sleep(1)
        self.readExcelAndFillData()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def readExcelAndFillData(self):
        try:
            global df
            df = pd.read_excel(self.fileName)
            self.temp_df = pd.DataFrame()

            for ind in df.index:
                try:
                    lpmno = df['lpmno'][ind]
                    lpmext = df['lpmext'][ind]
                    base_survey_no = df['base_survey_no'][ind]
                    sd_no = df['sd_no'][ind]

                    land_nature_webland = df['land_nature_webland'][ind]
                    total_ext = dp["total_ext"][ind]
                    land_classification = df['land_classification'][ind]
                    land_nature_broad_cat = df['land_nature_broad_cat'][ind]
                    land_nature_sub_cat = df["land_nature_sub_cat"][ind]
                    land_nature_sub_cat_two = df["land_nature_sub_cat_two"][ind]

                    land_classification_broad_cat = df["land_classification_broad_cat"][ind]
                    land_classification_sub_cat = df['land_classification_sub_cat'][ind]
                    land_classification_sub_cat_two = df["land_classification_sub_cat_two"][ind]
                    land_usage = df['land_usage'][ind]
                    source_of_irrigation = df['source_of_irrigation'][ind]
                    katha_num = df['katha_num'][ind]
                    pattadhar_name = df['pattadhar_name'][ind]
                    relation_name = df['relation_name'][ind]
                    succession = df['succession'][ind]
                    how_aquired = df['how_acquired'][ind]

                    if str(df['status'][ind]).lower() != "completed":
                            response = self.addRecordHelper(ind, lpmno, lpmext, base_survey_no, sd_no, land_nature_webland,total_ext, land_classification, land_nature_broad_cat, land_nature_sub_cat, land_nature_sub_cat_two, land_classification_broad_cat,land_classification_sub_cat,land_classification_sub_cat_two,land_usage, source_of_irrigation,katha_num, pattadhar_name, relation_name  )
                            if response:
                                df.at[ind, 'status'] = "Completed"
                            else:
                                df.at[ind, 'status'] = "Incomplete"
                    else:
                        print(str(lpmno) , " is already completed")
                    print("reached end!!")
                except Exception as e:
                    df.at[ind, 'status'] = "Incomplete"
                    print("Error in LPM ", str(lpmno)," with error", e)
                    # inner_warning_dialog = WarningDialog("Error in entering data of LPM number: ", str(lpmno))
                    # inner_warning_dialog.exec_()
                finally:
                    time.sleep(2)
                    # self.driver.refresh()
                    continue
        except Exception as e:
            print("Program terminated, Please restart the program", e)
            warning_dialog = WarningDialog("Program terminated, Please restart the program")
            warning_dialog.exec_()
        finally:
            with pd.ExcelWriter(self.fileName, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    home = AddRecordScreen()
    home.show()
    sys.exit(app.exec_())
