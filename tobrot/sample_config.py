import os

class Config(object):
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("1232917344:AAFc9RDuTFHECvYtHGIqPbqs89Qqm7HWzYI", "")
    # The Telegram API things
    APP_ID = int(os.environ.get("1596837", 12345))
    API_HASH = os.environ.get("9bed0cc5f4afae75fa05813a02a0a1b8")
    # Get these values from my.telegram.org
    # array to store the channel ID who are authorized to use the bot
    AUTH_CHANNEL = set(int(x) for x in os.environ.get("-1001205728332", "").split())
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 50000000
    TG_MAX_FILE_SIZE = 2097152000
    FREE_USER_MAX_FILE_SIZE = 50000000
    # chunk size that should be used with requests
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = 3600
    #
    ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", 6800))
    EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", 1))
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 600))
    MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", 1072864000))
    # add config vars for the display progress
    FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "█")
    UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "░")
    # add offensive API
    TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
    # URL for the rclone configuration
    R_CLONE_CONF_URI = os.environ.get("R_CLONE_CONF_URI", None)
