"""
Definition of a web scrapper class for getting free parking lots data
Author: Emmanuel Larralde
"""

from typing import Any, Iterator
from bs4 import BeautifulSoup
import requests

from misc import logger

class Requester:
    """
    Requests parking lots data from ISSEG Car parks' website
    """
    __estacionamientos = [
        'Gto-Alhondiga',
        'Gto-Alonso',
        'Gto-Hinojo',
        'Gto-Pozuelos',
        'Gto-SanPedro',
        'Irapuato-Hidalgo',
        'Leon-Mariachi'
    ]
    __URL = "https://estacionamientos.isseg.gob.mx:8070/SAE/GetDisponibilidad"
    def __init__(self, url: str = "") -> None:
        if url == "":
            url = Requester.__URL
        self.url = url

    def __call__(self, *args: Any, **kwargs: Any) -> Iterator[dict]:
        """
        Iterator. Returns up to date data of parking lots
        """
        while True:
            data = self.step()
            yield data

    def step(self) -> dict:
        """
        Requests parking load data via http
        """
        response = requests.get(self.url, timeout=10)
        if response.status_code != 200:
            return {}
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            # encontrar los estacionamientos
            estacionamientos = soup.find_all("div", class_="box")
            html_objects = []
            for estacionamiento in estacionamientos:
                cantidad = estacionamiento.find("span", class_="disponibles cantidad").text.strip()
                enlace = estacionamiento.find("a")["href"]
                html_objects.append((cantidad, enlace))

            data = {
                self.__estacionamientos[i - 1]: cantidad
                for i, (cantidad, _) in enumerate(html_objects, 1)
            }
        except Exception as e:
            logger.warning(e)
            return {}
        return data

    def finish(self) -> None:
        """
        Properly quits requesting. Does nothing. Added to follow prev pattern
        """
        return
