# import schedule
# import time

# from updater import Updater
# from updater.parsers import BS_RESOURCES, SELENIUM_RESOURCES, BUTTON_RESOURCES

# updater = Updater('config.yaml')
# updater._run()


# def update():
#     for resource_dict in BS_RESOURCES:
#         updater.bs_parse(**resource_dict)

#     for resource_dict in SELENIUM_RESOURCES:
#         updater.selenium_parse(**resource_dict)

#     for resource_dict in BUTTON_RESOURCES:
#         updater.button_parse(**resource_dict)


# schedule.every().day.at("09:00").do(update)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# updater.py (обновленный)


import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from updater import Updater
from updater.parsers import BS_RESOURCES, SELENIUM_RESOURCES, BUTTON_RESOURCES
import time

import sys
print(sys.executable)


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Инициализация Updater
updater = Updater('config.yaml')

def update():
    """Функция для обновления ресурсов."""
    logger.info("Запуск функции обновления")
    try:
        for resource_dict in BS_RESOURCES:
            updater.bs_parse(**resource_dict)
        for resource_dict in SELENIUM_RESOURCES:
            updater.selenium_parse(**resource_dict)
        for resource_dict in BUTTON_RESOURCES:
            updater.button_parse(**resource_dict)
        logger.info("Обновление завершено успешно")
    except Exception as e:
        logger.error(f"Ошибка во время обновления: {e}")

# Инициализация планировщика
scheduler = BackgroundScheduler()

# Настройка задачи на ежедневное выполнение в 09:34
scheduler.add_job(update, CronTrigger(hour=10, minute=16))

# Запуск планировщика
scheduler.start()
logger.info("Планировщик задач запущен")

# Основной цикл работы приложения
if __name__ == "__main__":
    try:
        while True:
            logger.info(f"Скрипт работает. Текущее время: {datetime.now()}")
            time.sleep(60)  # Проверка каждую минуту
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Скрипт остановлен")


