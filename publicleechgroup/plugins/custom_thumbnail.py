#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Copyright (C) 2020 PublicLeech Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from PIL import Image
from publicleechgroup import DOWNLOAD_LOCATION
from publicleechgroup.amocmadin import Loilacaztion


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
        await ismgs.edit(Loilacaztion.HELP_SAVE_THUMBNAIL)


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
