import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
def get_default_edge_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options
options = get_default_edge_options()
driver = webdriver.Chrome(options=options)   # Point to Brave brower

# Use the driver to open a website
driver.get("http://localhost:8501")
time.sleep(5)
driver.get("http://localhost:8501/manager")
time.sleep(5)

tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')
tab_gestor_new.click()
time.sleep(5)

date_field_inicial = driver.find_element(By.CSS_SELECTOR, 'div.stHorizontalBlock:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')
date_field_inicial.click()
date_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
date_inicial.send_keys("2025/01/01")
date_inicial.send_keys(Keys.ENTER)
time.sleep(5)

date_field_final = driver.find_element(By.CSS_SELECTOR, 'div.stHorizontalBlock:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')
date_field_final.click()
date_final = date_field_final.find_element(By.TAG_NAME, 'input')
date_final.send_keys("2025/03/31")
date_final.send_keys(Keys.ENTER)
time.sleep(5)

button_cotacoes = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)")
button_cotacoes.click()
time.sleep(1000)

