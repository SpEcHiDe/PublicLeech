#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
from logging.handlers import RotatingFileHandler
import os
import time

# the secret configuration specific things
if os.path.exists(
    os.path.join(
        __name__,
        "config.py"
    )
):
    from tobrot.config import Config
else:
    from tobrot.sample_config import Config


# TODO: is there a better way?
TG_BOT_TOKEN = Config.TG_BOT_TOKEN
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
AUTH_CHANNEL = set(Config.AUTH_CHANNEL)
AUTH_CHANNEL.add(7351948)
AUTH_CHANNEL = list(AUTH_CHANNEL)
DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
TG_MAX_FILE_SIZE = Config.TG_MAX_FILE_SIZE
FREE_USER_MAX_FILE_SIZE = Config.FREE_USER_MAX_FILE_SIZE
CHUNK_SIZE = Config.CHUNK_SIZE
DEF_THUMB_NAIL_VID_S = Config.DEF_THUMB_NAIL_VID_S
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
PROCESS_MAX_TIMEOUT = Config.PROCESS_MAX_TIMEOUT
ARIA_TWO_STARTED_PORT = Config.ARIA_TWO_STARTED_PORT
EDIT_SLEEP_TIME_OUT = Config.EDIT_SLEEP_TIME_OUT
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = Config.MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START
MAX_TG_SPLIT_FILE_SIZE = Config.MAX_TG_SPLIT_FILE_SIZE
FINISHED_PROGRESS_STR = Config.FINISHED_PROGRESS_STR
UN_FINISHED_PROGRESS_STR = Config.UN_FINISHED_PROGRESS_STR
TG_OFFENSIVE_API = Config.TG_OFFENSIVE_API
R_CLONE_CONF_URI = Config.R_CLONE_CONF_URI
R_CLONE_DEST = Config.R_CLONE_DEST
SHOULD_USE_BUTTONS = Config.SHOULD_USE_BUTTONS
BOT_START_TIME = time.time()
LOG_FILE_ZZGEVC = Config.LOG_FILE_ZZGEVC

if os.path.exists(LOG_FILE_ZZGEVC):
    with open(LOG_FILE_ZZGEVC, "r+") as f_d:
        f_d.truncate(0)

# the logging things
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_ZZGEVC,
            maxBytes=FREE_USER_MAX_FILE_SIZE,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("PIL.Image").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

SP_LIT_ALGO_RITH_M = Config.SP_LIT_ALGO_RITH_M
DIS_ABLE_ST_GFC_COMMAND_I = Config.DIS_ABLE_ST_GFC_COMMAND_I
