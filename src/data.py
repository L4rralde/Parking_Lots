"""
Code to load stored parking lot data
Author: Emmanuel Larralde
"""

from datetime import datetime
import os

import pandas as pd

from misc import GIT_ROOT, logger


class Data:
    """
    Class to manage parking lot datas with csv files and pandas
    """
    __dir_path = f"{GIT_ROOT}/data/" #Path of data directory
    def __init__(self) -> None:
        self.df = pd.read_csv(f"{self.__dir_path}/data.csv")
        self.df = self.df.loc[:, ~self.df.columns.str.contains('^Unnamed')]
        df_cp = pd.DataFrame(self.df)
        if not os.path.exists(f"{self.__dir_path}/backups/"):
            os.makedirs(f"{self.__dir_path}/backups/")
        df_cp.to_csv(
            f"{self.__dir_path}/backups/data.{str(datetime.now())}.csv"
        )
        self.cnt = 1

    def append(self, d: dict) -> None:
        """
        Appends new parking lot data
        """
        if not d:
            return
        new_d = {
            key: [value]
            for key, value in d.items()
        }
        new_d["Fecha_Hora"] = [datetime.now()]
        new_row = pd.DataFrame(new_d)
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.cnt = (self.cnt + 1) % 10
        if self.cnt == 0:
            self.save()

    def save(self) -> None:
        """
        Writes back new data to csv file
        """
        logger.info("Saving data")
        self.df.to_csv(f"{self.__dir_path}/data.csv")

    def finish(self) -> None:
        """
        Saves the data when program finishes
        """
        self.save()
