from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Acessa a página do gestor
        driver.get("http://localhost:8501/manager")
        
        time.sleep(5)
        
        driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)
        # driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)
        # driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)

        relatorio_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Relatório de Cotações')]")
        ))
        relatorio_button.click()
        time.sleep(2)
        
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        
        start_month = "Janeiro"
        driver.switch_to.active_element.send_keys(start_month)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        
        start_year = "2024"
        driver.switch_to.active_element.send_keys(start_year)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        
        end_month = "Março"
        driver.switch_to.active_element.send_keys(end_month)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        
        end_year = "2025"
        driver.switch_to.active_element.send_keys(end_year)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        
        researcher = "Cristina"
        driver.switch_to.active_element.send_keys(researcher)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.PAGE_DOWN)
        
        time.sleep(5)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
