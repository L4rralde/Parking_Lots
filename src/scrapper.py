from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://estacionamientos.isseg.gob.mx:8070/"


class Scrapper:
    __estacionamientos = [
        "Gto-Alhondiga",
        "Gto-Alonso",
        "Gto-Hinojo",
        "Gto-Pozuelos",
        "Gto-SanPedro",
        "Irapuato-Hidalgo",
        "Leon-Mariachi",
    ]
    def __init__(self, url: str = URL) -> None:
        self.url = url
        self.driver = webdriver.Chrome()

    def __call__(self, *args, **kwargs):
        self.driver.get(self.url)
        while True:
            self.pre_step(*args, **kwargs)
            data = self.step(*args, **kwargs)
            self.post_step(*args, **kwargs)
            yield data
            self.driver.refresh()

    def step(self, *args, **kwargs) -> dict:
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
            print(e)
            return {}
        return data

    def pre_step(self, *args, **kwargs) -> None:
        pass

    def post_step(self, *args, **kwargs) -> None:
        pass

    def finish(self, *args, **kwargs) -> None:
        self.driver.quit()
