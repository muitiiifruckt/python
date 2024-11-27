from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging

# Установка ожиданий в процессе работы
TIME_WAIT_BETWEEN_OPEN_NEW_WINDOW = 3
TIME_WAIT_FOR_FULL_LOADIND = 1

# Настройка параметров браузера
options = Options()
options.add_argument("--headless")  # Режим фона
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Текст для поиска
    search_text = "Иванов Иван Иванович"

    # URL сайта
    url = "https://bankrot.fedresurs.ru"

    # Настройка Selenium
    logger.info("Запуск браузера")
    driver = webdriver.Chrome()  # Убедитесь, что драйвер установлен и находится в PATH
    driver.maximize_window()

    try:
        logger.info(f"Переход на сайт: {url}")
        driver.get(url)

        # Поиск элемента ввода
        logger.info("Поиск поля для ввода текста")
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='searchString']"))
        )
        input_box.send_keys(search_text)
        logger.info(f'Текст "{search_text}" введен в поле ввода')

        # Нажатие Enter
        input_box.send_keys(Keys.RETURN)

        # Ожидание загрузки результатов
        logger.info("Ожидание загрузки результатов")
        results_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "app-bankrupt-result-persons"))
        )

        # Найти все элементы с селектором el-info-link .info_position
        info_links = driver.find_elements(By.CSS_SELECTOR, "el-info-link .info_position")



        # Получаем количество найденных элементов
        num_info_links = len(info_links)
        logger.info(f"Количество кнопок 'Вся информация': {num_info_links}")
        for i, link in enumerate(info_links):
            try:
                driver.execute_script("arguments[0].click();", link)
                print(f"Клик по кнопке {i + 1} из {len(info_links)}")
                time.sleep(TIME_WAIT_BETWEEN_OPEN_NEW_WINDOW)


                # Переключаемся на новую вкладку
                new_window = driver.window_handles[1]
                driver.switch_to.window(new_window)

                # Извлекаем нужные данные

                inn = driver.find_element(By.XPATH,
                                          "//div[contains(@class, 'identifier-name') and text()=' ИНН ']/following-sibling::div").text
                snils = driver.find_element(By.XPATH,
                                            "//div[contains(@class, 'identifier-name') and text()=' СНИЛС ']/following-sibling::div").text
                dob = driver.find_element(By.XPATH,
                                          "//div[contains(@class, 'info-item-name') and text()=' Дата рождения ']/following-sibling::div").text
                birth_place = driver.find_element(By.XPATH,
                                                  "//div[contains(@class, 'info-item-name') and text()=' Место рождения ']/following-sibling::div").text
                residence = driver.find_element(By.XPATH,
                                                "//div[contains(@class, 'info-item-name') and text()=' Место проживания ']/following-sibling::div").text

                # Вывод результатов
                print("ИНН:", inn)
                print("СНИЛС:", snils)
                print("Дата рождения:", dob)
                print("Место рождения:", birth_place)
                print("Место проживания:", residence)

                time.sleep(TIME_WAIT_FOR_FULL_LOADIND)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print(f"Ошибка при клике на элемент {i + 1}: {e}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        logger.info("Закрытие браузера")
        driver.quit()

if __name__ == "__main__":
    main()
