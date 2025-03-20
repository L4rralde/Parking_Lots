"""
Static module of miscellaneous code for the project
Author: Emmanuel Larralde
"""

import os
import sys
import logging
from datetime import datetime
from pytz import timezone

import git


tz = timezone("America/Mexico_City")


def now() -> datetime:
    """
    Returns now datetime with the desired format
    """
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")


git_repo = git.Repo(__file__, search_parent_directories=True)
GIT_ROOT = git_repo.git.rev_parse("--show-toplevel") #Root directory path

if not os .path.exists(f"{GIT_ROOT}/logs"): #Logs directory
    os.makedirs(f"{GIT_ROOT}/logs")

#Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
__fh = logging.FileHandler(f"{GIT_ROOT}/logs/{now()}.log")

__ch = logging.StreamHandler(sys.stdout)
__ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(name)s - %(levelname)s - %(message)s'
)
__ch.setFormatter(formatter)
__fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(__ch)
logger.addHandler(__fh)
