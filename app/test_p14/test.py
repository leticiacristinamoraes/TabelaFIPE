import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def get_default_edge_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

options = get_default_edge_options()
driver = webdriver.Chrome(options=options)  

# Abrir site
driver.get("http://localhost:8501")
time.sleep(5)
driver.get("http://localhost:8501/manager")
time.sleep(5)

# Acessar aba de gestor
tab_gestor_new = driver.find_element(By.ID, 'tabs-bui2-tab-4')
tab_gestor_new.click()
time.sleep(5)

# Datas de início e fim para os testes
datas_teste = [
    ("None", "None"),
    ("2024/01/01", "2025/01/01"),
    ("2025/01/01", "2024/01/01"),
    ("2025/05/01", "2025/06/01"),
    ("2025/03/02", "2025/03/02")
]

for i, (data_inicial, data_final) in enumerate(datas_teste, start=1):
    try:
        # Preencher data inicial
        date_field_inicial = driver.find_element(By.CSS_SELECTOR, 'div.stHorizontalBlock:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')
        date_field_inicial.click()
        date_input_inicial = date_field_inicial.find_element(By.TAG_NAME, 'input')
        date_input_inicial.send_keys(data_inicial)
        date_input_inicial.send_keys(Keys.ENTER)
        time.sleep(2)

        # Preencher data final
        date_field_final = driver.find_element(By.CSS_SELECTOR, 'div.stHorizontalBlock:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')
        date_field_final.click()
        date_input_final = date_field_final.find_element(By.TAG_NAME, 'input')
        date_input_final.send_keys(data_final)
        date_input_final.send_keys(Keys.ENTER)
        time.sleep(2)

        # Clicar no botão
        button_ranking = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)")
        button_ranking.click()


        time.sleep(10)
        print(f"Teste {i} - Data Inicial: {data_inicial}, Data Final: {data_final}: APROVADO ✅")

    except Exception as e:
        print(f"Teste {i} - Data Inicial: {data_inicial}, Data Final: {data_final}: REPROVADO ❌ - Erro: {e}")

driver.quit()


