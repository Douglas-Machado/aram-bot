from selenium import webdriver
from selenium.webdriver.common.by import By
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class AramDetails():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.keys = ["name", "winrate", "matches"]

    def get_top_ten_champions(self, total: int):
        self.driver.get(getenv("URL"))
        rows = self.driver.find_elements(By.CLASS_NAME, "rt-tr")
        rows.pop(0)
        rows = rows[:total]
        items = []
        for row in rows:
            values = row.text.split('\n')
            values.pop(4)
            values.pop(2)
            values.pop(0)
            items.append(values)

        self.driver.close()
        response_dict = [{k:v for (k,v) in zip(self.keys, infos)} for infos in items]
        return response_dict
