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


    
    def test_0_manager_should_open_tab_cotacoes_loja_error(self):
    #Tab de cotações da loja ainda não existe
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()

    def test_1_manager_should_open_tab_cotacoes_loja_success(self):
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()

    def test_2_manager_should_be_able_to_input_store_and_data_to_consult_error(self):
        #campos ainda não existem na pagina.
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()
        store_select = driver.find_element(By.CLASS_NAME, 'stores_options')
        
        date_field_inicial = driver.find_element(By.CLASS_NAME, 'data-inicial')

        date_field_final = driver.find_element(By.CLASS_NAME, 'data-final')
        
    def test_3_manager_should_be_able_to_input_store_and_data_to_consult_error_2(self):
        #campos ainda não existem na pagina.
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()
        #esse teste dá erro pelo fato de ele não achar o elemento que estamos procurando.
        #logo necessidade de criar keys para cada elemento e investigar como o streamlit usa o html.
        store_select = driver.find_element(By.CLASS_NAME, 'stores_options')
        
        date_field_inicial = driver.find_element(By.CLASS_NAME, 'data-inicial')

        date_field_final = driver.find_element(By.CLASS_NAME, 'data-final')

    def test_4_manager_should_be_able_to_input_store_and_data_to_consult_error_3(self):
        #campos existem mas erro acontece pois é necessario para cada campo dar um tempo de espera 
        #e usar enter para o streamlit enviar o input para o html
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()
        #
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("AutoCar")

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2025/01/01")

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2025/03/31")

        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        button_cotacoes.find_element(By.TAG_NAME, 'button').click()
        

    def test_5_manager_should_be_able_to_input_store_and_data_to_consult_success(self):
        #campos ainda não existem na pagina.
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("AutoCar")
        selected.send_keys(Keys.ENTER)
        time.sleep(3)

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2025/01/01")
        date_inicial.send_keys(Keys.ENTER)
        time.sleep(3)

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2025/01/31")
        date_final.send_keys(Keys.ENTER)
        time.sleep(3)

        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        button_cotacoes.find_element(By.TAG_NAME, 'button').click()
        

    def test_6_manager_should_be_able_to_input_store_and_data_to_consult_with_different_months_success(self):
        #campos ainda não existem na pagina.
        driver = self.driver
        driver.get("http://localhost:8501")
        time.sleep(5)

        tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')

        tab_gestor_new.click()
        tab_select = driver.find_element(By.CLASS_NAME, 'st-key-stores_options')
        list_select = tab_select.find_element(By.CSS_SELECTOR, 'div[data-baseweb="select"]')
        selected = list_select.find_element(By.TAG_NAME, 'input')
        selected.send_keys("AutoCar")
        selected.send_keys(Keys.ENTER)
        time.sleep(3)

        date_field_inicial = driver.find_element(By.CLASS_NAME, 'st-key-data-inicial')
        date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_inicial.send_keys("2025/01/01")
        date_inicial.send_keys(Keys.ENTER)
        time.sleep(3)

        date_field_final = driver.find_element(By.CLASS_NAME, 'st-key-data-final')
        date_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_final.send_keys("2025/03/31")
        date_final.send_keys(Keys.ENTER)
        time.sleep(3)

        button_cotacoes = driver.find_element(By.CLASS_NAME, "st-key-button-cotacoes")
        
        waiting = WebDriverWait(driver,10)
        button_cotacoes_clickable=waiting.until(EC.element_to_be_clickable(button_cotacoes.find_element(By.TAG_NAME, 'button')))
        button_cotacoes_clickable.click()
        #canvas class name stVegaLiteChart

# Use the driver to open a website
    def tearDown(self):
        time.sleep(30)
        self.driver.quit()

      
if __name__ == '__main__': 
    unittest.main()