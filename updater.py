import schedule
import time

from updater import Updater
from updater.parsers import BS_RESOURCES, SELENIUM_RESOURCES, BUTTON_RESOURCES

updater = Updater('config.yaml')
updater._run()


def update():
    for resource_dict in BS_RESOURCES:
        updater.bs_parse(**resource_dict)

    for resource_dict in SELENIUM_RESOURCES:
        updater.selenium_parse(**resource_dict)

    for resource_dict in BUTTON_RESOURCES:
        updater.button_parse(**resource_dict)


schedule.every().day.at("11:28").do(update)
while True:
    schedule.run_pending()
    time.sleep(1)
