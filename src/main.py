from time import sleep

from scrapper import Scrapper
from data import Data


def main():
    scrapper = Scrapper()
    db = Data()
    try:
        for data in scrapper():
            print(data)
            db.append(data)
            sleep(10)
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        print("Finishing program")
        scrapper.finish()
        db.finish()


if __name__ == '__main__':
    main()
