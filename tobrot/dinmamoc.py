import os


class Commandi:
    LEECH = os.environ.get(
        "COMMANDI_LEECH",
        "leech"
    )
    PURGE = os.environ.get(
        "COMMANDI_PURGE",
        "purge"
    )
    YTDL = os.environ.get(
        "COMMANDI_YTDL",
        "ytdl"
    )
    STATUS = os.environ.get(
        "COMMANDI_STATUS",
        "status"
    )
    CANCEL = os.environ.get(
        "COMMANDI_CANCEL",
        "cancel"
    )
    EXEC = os.environ.get(
        "COMMANDI_EXEC",
        "exec"
    )
    RENAME = os.environ.get(
        "COMMANDI_RENAME",
        "rename"
    )
    UPLOAD = os.environ.get(
        "COMMANDI_UPLOAD",
        "upload"
    )
    HELP = os.environ.get(
        "COMMANDI_HELP",
        "help"
    )
    SAVETHUMBNAIL = os.environ.get(
        "COMMANDI_SAVETHUMBNAIL",
        "savethumbnail"
    )
    CLEARTHUMBNAIL = os.environ.get(
        "COMMANDI_CLEARTHUMBNAIL",
        "clearthumbnail"
    )
    GET_RCLONE_CONF_URI = os.environ.get(
        "COMMANDI_GET_RCLONE_CONF_URI",
        "getrcloneconfuri"
    )
