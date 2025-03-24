from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def test_pesquisador_invalido():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Acessa a página do gestor
        driver.get("http://localhost:8501/manager")
        time.sleep(5)

        driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)

        # Clica no botão "Relatório de Cotações"
        relatorio_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Relatório de Cotações')]"))
        )
        relatorio_button.click()
        time.sleep(2)

        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.TAB)

        # Seleciona Mês Inicial
        start_month = "Janeiro"
        driver.switch_to.active_element.send_keys(start_month)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)

        # Seleciona Ano Inicial
        start_year = "2024"
        driver.switch_to.active_element.send_keys(start_year)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)

        # Seleciona Mês Final
        end_month = "Março"
        driver.switch_to.active_element.send_keys(end_month)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)

        # Seleciona Ano Final
        end_year = "2025"
        driver.switch_to.active_element.send_keys(end_year)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)

        # Digita um pesquisador inexistente
        pesquisador_invalido = "Pesquisador Inexistente"
        driver.switch_to.active_element.send_keys(pesquisador_invalido)

        time.sleep(3)

        # Verifica se uma mensagem de erro/aplicação avisa que a entrada é inválida
        try:
            error_message = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Nenhuma cotação encontrada')]"))
            )
            print("Teste passou: O sistema retornou mensagem de erro ao inserir um pesquisador inválido.")
        except:
            print("Teste falhou: O sistema permitiu pesquisar com um pesquisador inválido.")

        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    test_pesquisador_invalido()
