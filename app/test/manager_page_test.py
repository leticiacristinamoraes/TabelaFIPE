import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
def get_default_edge_options():
    options = webdriver.EdgeOptions()
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options
options = get_default_edge_options()
driver = webdriver.Edge(options=options)   # Point to Brave brower
# options.add_argument('--headless')      # Optional: Run brower in headless mode

# Create a Service object
# service = Service()

# Create a WebDriver instance

# Use the driver to open a website
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
button_cotacoes.find_element(By.TAG_NAME, 'button').click()
time.sleep(1000)

