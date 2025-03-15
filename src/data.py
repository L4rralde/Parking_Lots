from datetime import datetime
import os

import pandas as pd
import git

git_repo = git.Repo(__file__, search_parent_directories=True)
git_root = git_repo.git.rev_parse("--show-toplevel")

class Data:
    __dir_path = f"{git_root}/data/"
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
        print("Saving data")
        self.df.to_csv(f"{self.__dir_path}/data.csv")

    def finish(self) -> None:
        self.save()
