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


class Auto:
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


if __name__ == '__main__':
    auto = Auto("driver/chromedriver.exe")
    auto.run()
