import time
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


def openBrowser():
    driver = webdriver.Chrome()
    driver.get("https://webland2.ap.gov.in/POLR6/loginpage.aspx")
    time.sleep(1)
    driver.maximize_window()
    time.sleep(20000)
    # "https://webland2.ap.gov.in/POLR6/loginpage.aspx"


def openAddRecordPage():
    driver.get("https://webland2.ap.gov.in/POLR6/NewProcess/DraftLandRegister.aspx")
    # "https://webland2.ap.gov.in/POLR6/NewProcess/DraftLandRegister.aspx"


def selectVillage():
    time.sleep(0.5)
    dddlvillage = driver.find_element(By.XPATH, '//*[@id="ddlvillage"]')
    # ddlvillage = driver.find_element(By.xpath,'//*[@id="ddlvillage"]')
    select_object = Select(dddlvillage)
    # for selecting Pedapudi village 1609036
    select_object.select_by_value('1623027')
    driver.find_element(By.XPATH, '//*[@id="btngetdetails"]').click()


def readExcel(path):
    df = pd.read_excel(path)
    return df
    # "E:\\automation\\DLR Insert Template_01102022.xlsx"
