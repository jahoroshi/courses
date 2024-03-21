from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Создаем экземпляр опций Chrome
chrome_options = Options()

# Устанавливаем параметр загрузки страницы без изображений
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")

# Создаем экземпляр браузера с заданными опциями
driver = webdriver.Chrome(options=chrome_options)

# Открываем страницу
driver.get('https://www.wildberries.by/catalog?search=%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%B0&tail-location=SNT&page=2')
time.sleep(10)

# Ждем, пока страница полностью не загрузится
driver.implicitly_wait(10)

# Сохраняем результат в файл
with open('page.html', 'w') as f:
    f.write(driver.page_source)

# Закрываем браузер
driver.quit()
