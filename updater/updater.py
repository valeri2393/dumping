import logging
import re
import requests
import sqlite3
import time
# import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from lxml import etree
from datetime import date

from util.config import build_config
from util.db import request_sql, get_cards_info


class Updater():
    def __init__(self, cfg_path: str):
        cfg = build_config(cfg_path)
        self._conn = sqlite3.connect(cfg["DBPath"])
        self._logger = Updater._new_logger(cfg["UpdaterLogPath"])

    def _run(self):
        self._logger.info("Начало работы")

    def _new_logger(logpath: str):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logpath, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s") # noqa
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _log(self, message):
        self._logger.info(message)

    def _update(self, result: list):
        date_today = date.today().strftime("%d.%m.%Y")
        for row in result:
            id = int(row[0])
            price = re.sub(r'[^\d\.\,)]', '', str(row[1])).rstrip(".")
            cursor = self._conn.cursor()
            query = "DELETE FROM prices " +\
                    f"WHERE id = {id} AND date = '{date_today}'"
            cursor.execute(query)
            query = "INSERT INTO prices(id, date, price) VALUES (?, ?, ?)"
            cursor.execute(query, (id, date_today, price))
        self._conn.commit()
        cursor.close()

    def bs_parse(self, resource: str, path: str, attr='text'):
        urls, ids = get_cards_info(self._conn, resource)
        self._log(f"Обновление цен ресурса: {resource}")
        prices = []
        for i in range(len(urls)):
            try:
                page = requests.get(urls[i])
                soup = BeautifulSoup(page.text, "html.parser")
                dom = etree.HTML(str(soup))
                pr = dom.xpath(path)[0]
                price = pr.text if attr == 'text' else pr.get(attr)
            except Exception as e:
                price = 0
                self._log(
                    f"Ошибка обновления! Ресурс: {resource}, id: {ids[i]}," +
                    f" ссылка: {urls[i]}, ошибка: {e}"
                )
            prices.append(price)
        self._update(list(zip(ids, prices)))

    def selenium_parse(
            self,
            resource: str,
            path: str,
            attr='textContent',
            sleep_time=0.1,
    ):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'

        driver = webdriver.Chrome(
            options=options,
            # version_main=122
        )
        urls, ids = get_cards_info(self._conn, resource)
        self._log(f"Обновление цен ресурса: {resource}")
        prices = []
        for i in range(len(urls)):
            try:
                driver.get(urls[i])
                time.sleep(sleep_time)
                price = driver.find_element(By.XPATH, path).get_attribute(attr)
            except Exception as e:
                price = 0
                self._log(
                    f"Ошибка обновления! Ресурс: {resource}, id: {ids[i]}," +
                    f" ссылка: {urls[i]}, ошибка: {e}"
                )
            prices.append(price)
        driver.quit()
        self._update(list(zip(ids, prices)))

    def button_parse(
            self,
            resource: str,
            buttons_path: str,
            price_path: str,
            del_index: list,
            sleep_time=3,
            attr='textContent',
            select_path=None
    ):
        query = f"SELECT DISTINCT url FROM cards WHERE resource = '{resource}'"
        urls = [el[0] for el in request_sql(self._conn, query)]

        ids = get_cards_info(self._conn, resource)[1]
        self._log(f"Обновление цен ресурса: {resource}")
        prices = []

        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(options=options)
        for url in urls:
            driver.get(url)
            time.sleep(sleep_time)
            if select_path:
                driver.find_element(By.XPATH, select_path).click()
            buttons = driver.find_elements(By.XPATH, buttons_path)
            for button in buttons:
                if select_path:
                    driver.find_element(By.XPATH, select_path).click()
                button.click()
                time.sleep(sleep_time)
                price = driver.find_element(By.XPATH, price_path).get_attribute(attr) # noqa
                prices.append(price)
        driver.quit()
        for ind in del_index:
            prices.pop(ind)
        self._update(list(zip(ids, prices)))
