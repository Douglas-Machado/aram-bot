from selenium import webdriver
from selenium.common.exceptions import NoSuchDriverException
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

load_dotenv()

class AramDetails:
    def __init__(self):
        self.keys = ["name", "winrate", "matches"]


    def get_top_champions(self, total: int):
        driver = self.get_default_browser()
        driver.get(os.getenv("ARAM_WEB_URL"))
        rows = driver.find_elements(By.CLASS_NAME, "rt-tr")
        rows.pop(0)
        rows = rows[:total]
        items = []
        for row in rows:
            values = row.text.split("\n")
            values.pop(4)
            values.pop(2)
            values.pop(0)
            items.append(values)

        driver.close()
        response_dict: [dict] = [{k: v for (k, v) in zip(self.keys, infos)} for infos in items]
        return response_dict
    
    def get_default_browser(self):
        try:
            return webdriver.Firefox()
        except NoSuchDriverException as ex:
            print('firefox')
            print(ex)
        try:
            return webdriver.Chrome()
        except NoSuchDriverException as ex:
            print('chrome')
            print(ex)
        try:
            return webdriver.Ie()
        except NoSuchDriverException as ex:
            print('IE')
            print(ex)
