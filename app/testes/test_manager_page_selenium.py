import datetime
import unittest
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class TestUIFeatureCotationStore(unittest.TestCase):
    
    def setUp(self):
        options = webdriver.EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(2)

# Create a WebDriver instance

    def test_0_input_store_and_data_to_consult_different_month(self):
        
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-9')

        tab_gestor_new.click()
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("AutoCar")
        selected.send_keys(Keys.ENTER)
        time.sleep(3)

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2024/11/01")
        date_inicial.send_keys(Keys.ENTER)
        date_inicial.send_keys(Keys.TAB)
        time.sleep(3)

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2025/02/28")
        date_final.send_keys(Keys.ENTER)
        date_final.send_keys(Keys.TAB)
        time.sleep(3)


        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        buttonms = button_cotacoes.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", buttonms)
        time.sleep(3)
        graphic = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="stVegaLiteChart"]')
        driver.execute_script("arguments[0].scrollIntoView();", graphic)
        time.sleep(30)


    def test_1_input_store_and_data_to_consult_with_date_final_before_date_start(self):
        #campos ainda não existem na pagina.
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-9')

        tab_gestor_new.click()
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("AutoCar")
        selected.send_keys(Keys.ENTER)
        time.sleep(3)

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2025/03/01")
        date_inicial.send_keys(Keys.ENTER)
        date_inicial.send_keys(Keys.TAB)
        time.sleep(3)

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2024/12/01")
        date_final.send_keys(Keys.ENTER)
        date_final.send_keys(Keys.TAB)
        time.sleep(3)


        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        buttonms = button_cotacoes.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", buttonms)
        time.sleep(3)
        graphic = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="stVegaLiteChart"]')
        driver.execute_script("arguments[0].scrollIntoView();", graphic)
        time.sleep(30)


    def test_2_input_store_and_data_to_consult_with_inexstent_store(self):

        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-9')

        tab_gestor_new.click()
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("NotExist")
        selected.send_keys(Keys.ENTER)
        selected.send_keys(Keys.TAB)
        time.sleep(3)

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2024/11/01")
        date_inicial.send_keys(Keys.ENTER)
        date_inicial.send_keys(Keys.TAB)
        time.sleep(3)

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2025/02/28")
        date_final.send_keys(Keys.ENTER)
        date_final.send_keys(Keys.TAB)
        time.sleep(3)


        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        buttonms = button_cotacoes.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", buttonms)
        time.sleep(3)
        graphic = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="stVegaLiteChart"]')
        driver.execute_script("arguments[0].scrollIntoView();", graphic)
        time.sleep(30)


    def test_3_input_store_and_data_to_consult_not_in_BD(self):
        #campos ainda não existem na pagina.
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-9')

        tab_gestor_new.click()
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("AutoCar")
        selected.send_keys(Keys.ENTER)
        selected.send_keys(Keys.TAB)
        time.sleep(3)

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2023/11/01")
        date_inicial.send_keys(Keys.ENTER)
        date_inicial.send_keys(Keys.TAB)
        time.sleep(3)

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2023/12/28")
        date_final.send_keys(Keys.ENTER)
        date_final.send_keys(Keys.TAB)
        time.sleep(3)


        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        buttonms = button_cotacoes.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", buttonms)
        time.sleep(3)
        graphic = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="stVegaLiteChart"]')
        driver.execute_script("arguments[0].scrollIntoView();", graphic)
        time.sleep(30)
# Use the driver to open a website
    def tearDown(self):
        self.driver.quit()

      
if __name__ == '__main__': 
    unittest.main()