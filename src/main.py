"""
Periodically scraps parking lot data from ISSEG's website
"""

from time import sleep

from scrapper import Scrapper
from data import Data
from misc import logger


def main() -> None:
    """
    Requests new data from web scrapper eavery minute.
    Saves the data
    """
    scrapper = Scrapper()
    db = Data()
    try:
        for data in scrapper():
            db.append(data)
            sleep(60)
    except KeyboardInterrupt:
        logger.info("Interrupted")
    finally:
        logger.info("Finishing program")
        scrapper.finish()
        db.finish()


if __name__ == '__main__':
    main()
