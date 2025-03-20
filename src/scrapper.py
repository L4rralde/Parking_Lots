"""
Definition of a web scrapper class for getting free parking lots data
Author: Emmanuel Larralde
"""
from collections.abc import Iterator
import abc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from misc import logger


class Scrapper:
    """
    Retrieves parking lots data from ISSEG Car parks' website
    """
    __estacionamientos = [ #All ISSEG Car parks
        "Gto-Alhondiga",
        "Gto-Alonso",
        "Gto-Hinojo",
        "Gto-Pozuelos",
        "Gto-SanPedro",
        "Irapuato-Hidalgo",
        "Leon-Mariachi",
    ]
    __URL = "https://estacionamientos.isseg.gob.mx:8070/"
    __DRIVER = "/opt/homebrew/bin/chromedriver"
    def __init__(self, url: str = "") -> None:
        if url == "":
            url = self.__URL
        self.url = url
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        service = Service(executable_path=self.__DRIVER)
        self.driver = webdriver.Chrome(service=service, options=options)

    def __call__(self, *args, **kwargs) -> Iterator[dict]:
        """
        Iterator. Returns up to date data of parking lots
        """
        self.driver.get(self.url)
        while True:
            self.__pre_step(*args, **kwargs)
            data = self.step()
            self.__post_step(*args, **kwargs)
            yield data
            self.driver.refresh()

    def step(self) -> dict:
        """
        Waits until web site is loaded and retrieves parking lots data
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            span_elements = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "span.disponibles.cantidad")
                )
            )
            data = {
                est: element.text
                for est, element in zip(self.__estacionamientos, span_elements)
            }
        except Exception as e:
            logger.warning(e)
            return {}
        return data

    @abc.abstractmethod
    def __pre_step(self, *args, **kwargs) -> None:
        """
        Abstract method
        """
        return

    @abc.abstractmethod
    def __post_step(self, *args, **kwargs) -> None:
        """
        Abstract method
        """
        return

    def finish(self) -> None:
        """
        Properly quits scrapping
        """
        self.driver.quit()
