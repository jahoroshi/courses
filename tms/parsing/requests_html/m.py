from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Создайте экземпляр веб-драйвера (например, Chrome)
driver = webdriver.Chrome()

try:
    # Откройте страницу по URL
    driver.get("https://www.wildberries.by/catalog?search=%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%B0&tail-location=SNT&page=2")
    time.sleep(20)


    # Дождитесь, пока элемент с id="my-element" станет видимым
    wait = WebDriverWait(driver, 25.2)
    driver.set_script_timeout(30)
    driver.set_page_load_timeout(30)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Получите HTML-код всей страницы
    page_source = driver.page_source

    # # Получите текст элемента
    result_text = element.text

    # Сохраните результат в файл
    with open("result.html", "w") as file:
        file.write(result_text)

finally:
    # Закройте веб-драйвер
    driver.quit()
