import sys
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



class LEMDeletion:
    def __init__(self):
        super().__init__()
        self.openBrowser()
    def openBrowser(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://webland2.ap.gov.in/POLR6/loginpage.aspx")
        time.sleep(1)
        self.driver.maximize_window()
        self.driver.find_element(By.XPATH, '//*[@id="useID"]').send_keys(str('jcankp001'))
        self.driver.find_element(By.XPATH, '//*[@id="pqrabc"]').send_keys(str('Indo12345'))
        # //*[@id="ddlDist"]
        try:
            # print("Option loaded")
            districtSelect = self.driver.find_element(By.XPATH, '//*[@id="ddlDist"]')
            distSel = Select(districtSelect)
            distSel.select_by_value('16')
        except TimeoutException:
            print("Time exceeded!")
        # Enter capcha and submit the form
        time.sleep(20)
        # self.selectVillage()
        self.openAddRecordPage()
        # "https://webland2.ap.gov.in/POLR6/loginpage.aspx"

    def openAddRecordPage(self):
        self.driver.get("https://webland2.ap.gov.in/POLR6/NewProcess/DraftLandRegister_RDOJC.aspx")
        # "https://webland2.ap.gov.in/POLR6/NewProcess/DraftLandRegister.aspx"
        self.selectVillage()

    def selectVillage(self):
        time.sleep(2)

        # select mandal
        ddlmandal = self.driver.find_element(By.XPATH, '// *[ @ id = "ddlmandal"]')
        select_object = Select(ddlmandal)
        select_object.select_by_value('23')
        time.sleep(1)
        # select village
        dddlvillage = self.driver.find_element(By.XPATH, '//*[@id="ddlvillage"]')
        select_object = Select(dddlvillage)
        select_object.select_by_value('1623012')
        self.driver.find_element(By.XPATH, '//*[@id="btngetdetails"]').click()
        time.sleep(1)
        self.delete_lpm()

    def delete_lpm(self):
        lpmDict = {}
        try:
            # print("Option loaded")
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ddlLPMno"]/option[8]'))
            )
            lpmNumberSelect = self.driver.find_element(By.XPATH, '//*[@id="ddlLPMno"]')
            lpmSelect = Select(lpmNumberSelect)
            for option in lpmSelect.options:
                kathas = option.text.strip().split('-')
                katha1 = kathas[0]
                katha2 = kathas[1]
                lpmDict[katha1] = option.text
                lpmDict[katha2] = option.text
            # KathaSelect.select_by_visible_text(kathaNumber)
        except TimeoutException:
            print("Time exceeded!")
        time.sleep(2)

        range_start = 6000
        range_end = 6003
        for currentLPM in range(range_start, range_end+1):
            print("at index", currentLPM)


            try:
                # print("Option loaded")
                lpmRange = lpmDict[str(currentLPM)]
                lpmRangeSelect = self.driver.find_element(By.XPATH, '//*[@id="ddlLPMno"]')
                rangeSel = Select(lpmRangeSelect)
                rangeSel.select_by_visible_text(lpmRange)
            except Exception:
                print("Exception in LPM", str(currentLPM))
                continue
            time.sleep(2)

            try:
                for i in range(1000):
                    try:
                        currLpmNumber = str(
                            self.driver.find_element(By.XPATH, '//*[@id="grgroundtruth_txtlpmno_' + str(i) + '"]').get_attribute(
                                'value')).strip()
                        if (str(currLpmNumber) == str(lpmno)):
                            self.driver.find_element(By.XPATH, '//*[@id="grgroundtruth_btnedit_' + str(i) + '"]').click()
                            time.sleep(3)
                            self.driver.find_element(By.XPATH,
                                                '// *[ @ id = "grgroundtruth_txtlpmnoExtent_' + str(i) + '"]').clear()

                            self.driver.find_element(By.XPATH,
                                                '//*[@id="grgroundtruth_txtlpmnoExtent_' + str(i) + '"]').send_keys(
                                '0.001')
                            driver.find_element(By.XPATH, '// *[ @ id = "grgroundtruth_btnsave_' + str(i) + '"]').click()
                            print(currLpmNumber, " Updated successfully!!")
                    except Exception:
                        print("Exception in lpmno", currLpmNumber)
                        continue

            except Exception:
                print("Lpm doesnt exist")
                continue



# if __name__ == '__main__':
#     lpm_deletion = LEMDeletion()
