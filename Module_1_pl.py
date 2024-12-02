import asyncio
from playwright.async_api import async_playwright
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_person_data(page):
    """
    Извлечение данных о человеке с текущей страницы.
    """
    try:
        # Ожидание появления элемента с датой рождения
        await page.wait_for_selector(
            "//div[contains(@class, 'info-item-name') and text()=' Дата рождения ']/following-sibling::div",
            timeout=30000)

        # Извлечение текста
        dob = await page.inner_text(
            "//div[contains(@class, 'info-item-name') and text()=' Дата рождения ']/following-sibling::div")

        # Логируем данные
        logger.info(f"""
        Данные о человеке:
        Дата рождения: {dob}

        """)
    except Exception as e:
        logger.error(f"Ошибка при извлечении данных: {e}")


async def process_search_results(context, info_links):
    """
    Обработка результатов поиска.
    """
    for i, link in enumerate(info_links):
        try:
            logger.info(f"Клик по кнопке {i + 1} из {len(info_links)}")
            await link.click()

            # Ожидание открытия новой вкладки или обработка текущей
            try:
                new_page = await context.wait_for_event("page", timeout=30000)
            except Exception:
                logger.warning("Переход выполнен в текущей вкладке")
                new_page = context.pages[-1]  # Используем последнюю открытую страницу

            await new_page.wait_for_load_state()
            await fetch_person_data(new_page)

            # Добавление небольшой паузы

            if new_page != context.pages[0]:
                await new_page.close()

        except Exception as e:
            logger.error(f"Ошибка при обработке элемента {i + 1}: {e}")


async def main():
    search_text = "Иванов Иван Иванович"
    url = "https://bankrot.fedresurs.ru"

    logger.info("Запуск Playwright")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        try:
            page = await context.new_page()
            logger.info(f"Переход на сайт: {url}")
            await page.goto(url)

            logger.info("Поиск поля для ввода текста")
            input_box = await page.query_selector("input[formcontrolname='searchString']")
            if not input_box:
                logger.error("Поле для ввода текста не найдено")
                return

            await input_box.fill(search_text)
            logger.info(f'Текст "{search_text}" введен в поле ввода')
            await input_box.press("Enter")

            logger.info("Ожидание загрузки результатов")
            await page.wait_for_selector("app-bankrupt-result-persons")

            info_links = await page.query_selector_all("el-info-link .info_position")
            logger.info(f"Найдено кнопок 'Вся информация': {len(info_links)}")

            if info_links:
                await process_search_results(context, info_links)
            else:
                logger.warning("Кнопки 'Вся информация' не найдены")

        except Exception as e:
            logger.error(f"Ошибка: {e}")
        finally:
            logger.info("Закрытие браузера")
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
