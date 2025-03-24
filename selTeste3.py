import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def get_default_edge_options():
    options = webdriver.EdgeOptions()
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

options = get_default_edge_options()
driver = webdriver.Edge(options=options)  


driver.get("http://localhost:8501/manager")  
time.sleep(25)
#Teste 3 -Teste de validação de período inválido

aba_produtividade = driver.find_element(By.ID, 'tabs-bui2-tab-4')
aba_produtividade.click()
time.sleep(5)


ano_inicial = driver.find_element(By.XPATH, '//*[@id="tabs-bui2-tabpanel-4"]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/input')
ano_inicial.send_keys("2025")  
ano_inicial.send_keys(Keys.ENTER)
time.sleep(2)

mes_inicial = driver.find_element(By.XPATH, '//*[@id="tabs-bui2-tabpanel-4"]/div/div/div/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/input')
mes_inicial.send_keys("5")
mes_inicial.send_keys(Keys.ENTER)
time.sleep(2)

ano_final = driver.find_element(By.XPATH, '//*[@id="tabs-bui2-tabpanel-4"]/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[2]/input')
ano_final.send_keys("2025")  
ano_final.send_keys(Keys.ENTER)
time.sleep(2)

mes_final = driver.find_element(By.XPATH, '//*[@id="tabs-bui2-tabpanel-4"]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[2]/input')
mes_final.send_keys("2")
mes_final.send_keys(Keys.ENTER)
time.sleep(2)





time.sleep(10)
driver.quit()
