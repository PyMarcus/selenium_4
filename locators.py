import time
from typing import List

from dotenv import load_dotenv
from os import getenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv(
    ".env"
)


class OrangeUser:
    link: str = getenv("URL")
    username: str = getenv("USER")
    password: str = getenv("PASSWORD")


class AutoLogin:
    def __init__(self, driver_path: str) -> None:
        self.__service = Service(driver_path)
        self.__driver: WebDriver = webdriver.Chrome(service=self.__service)

    def run(self) -> None:
        self.__driver.get(OrangeUser.link)
        username_component: WebElement = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_component: WebElement = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        button: WebElement = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-button"))
        )

        username_component.send_keys(OrangeUser.username)
        password_component.send_keys(OrangeUser.password)
        button.click()

        self.__capture_title()
        self.__driver.close()

    def __capture_title(self) -> None:
        print(f"Title captured: {self.__driver.title}")


class PathLocators:
    def __init__(self, driver_path: str) -> None:
        self.__service = Service(driver_path)
        self.__driver = webdriver.Chrome(service=self.__service)
        self.__driver.get(getenv("URL2"))

    def get_items_by_id(self, id: str) -> None:
        self.__driver.find_element(By.ID, id).send_keys('import')

    def search(self, class_name: str) -> None:
        self.__driver.find_element(By.CLASS_NAME, class_name).click()

    def access_item_by_link_text(self, text: str) -> None:
        self.__driver.find_element(By.LINK_TEXT, text).click()

    def access_item_by_link_partial_text(self, text: str) -> None:
        link: WebElement = self.__driver.find_element(By.PARTIAL_LINK_TEXT, text)
        print(f"LINK TEXT: {link.text}")
        print(f"LINK {link.get_attribute('href')}")
        link.click()

    def select_multiple_elements(self, class_name: str) -> None:
        elements: List[WebElement] = self.__driver.find_elements(By.CLASS_NAME, class_name)
        for element in elements:
            if element.text:
                print(f"ITEM: {element.text}")

    def get_elements_with_combination(self) -> None:
        self.__driver.get(OrangeUser.link)
        username: WebElement = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        ) # tag + name
        username.send_keys('test')

    def start(self) -> None:
        self.get_items_by_id("SearchTerm")
        self.search("button-marketplace-search")
        #self.access_item_by_link_text("Import/Export Products and Specification attributes")
        self.select_multiple_elements("custom-control-label")
        self.access_item_by_link_partial_text("Import/Export")
        self.get_elements_with_combination()
        time.sleep(5)
        self.__driver.close()

        self.__driver.quit()


if __name__ == '__main__':
    #auto = AutoLogin("driver/chromedriver.exe")
    #auto.run()
    path_locator = PathLocators("driver/chromedriver.exe")
    path_locator.start()
