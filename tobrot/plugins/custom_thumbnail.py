"""ThumbNail utilities, © @AnyDLBot"""

import os
from PIL import Image
from tobrot import DOWNLOAD_LOCATION
from tobrot.amocmadin import Loilacaztion


async def save_thumb_nail(_, message):
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION,
        "thumbnails"
    )
    thumb_image_path = os.path.join(
        thumbnail_location,
        str(message.from_user.id) + ".jpg"
    )
    ismgs = await message.reply_text(Loilacaztion.PROCESSING)
    if message.reply_to_message is not None:
        if not os.path.isdir(thumbnail_location):
            os.makedirs(thumbnail_location)
        download_location = thumbnail_location + "/"
        downloaded_file_name = await message.reply_to_message.download(
            file_name=download_location
        )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert(
            "RGB"
        ).save(downloaded_file_name)
        # ref: https://t.me/PyrogramChat/44663
        img = Image.open(downloaded_file_name)
        img.save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        await ismgs.edit(Loilacaztion.SAVED_THUMBNAIL)
    else:
        await message.edit(Loilacaztion.HELP_SAVE_THUMBNAIL)


async def clear_thumb_nail(_, message):
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION,
        "thumbnails"
    )
    thumb_image_path = os.path.join(
        thumbnail_location,
        str(message.from_user.id) + ".jpg"
    )
    ismgs = await message.reply_text(Loilacaztion.PROCESSING)
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await ismgs.edit(Loilacaztion.CLEARED_THUMBNAIL)
