#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  PublicLeech
#  Copyright (C) 2020 The Authors

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
import time

from pyrogram import (
    Message
)

from tobrot import (
    LOGGER,
    DOWNLOAD_LOCATION
)
from tobrot.helper_funcs.download_aria_p_n import (
    call_apropriate_function,
    aria_start,
    fake_etairporpa_call
)
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats


async def leech_btn_k(message: Message, cb_data: str):
    # get link from the incoming message
    dl_url, cf_name, _, _ = await extract_link(
        message.reply_to_message, "LEECH"
    )
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await message.edit_text("extracting links")
        # start the aria2c daemon
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        if "_" in cb_data:
            current_user_id = message.reply_to_message.from_user.id
            # create an unique directory
            new_download_location = os.path.join(
                DOWNLOAD_LOCATION,
                str(current_user_id),
                str(time.time())
            )
            # create download directory, if not exist
            if not os.path.isdir(new_download_location):
                os.makedirs(new_download_location)
            await message.edit_text("trying to download")
            # try to download the "link"
            sagtus, err_message = await fake_etairporpa_call(
                aria_i_p,
                dl_url,
                new_download_location,
                message,
                int(cb_data.split("_")[2])
                # maybe IndexError / ValueError might occur,
                # we don't know, yet!!
            )
            if not sagtus:
                # if FAILED, display the error message
                await message.edit_text(err_message)
        else:
            is_zip = False
            if "a" in cb_data:
                is_zip = True
            current_user_id = message.reply_to_message.from_user.id
            # create an unique directory
            new_download_location = os.path.join(
                DOWNLOAD_LOCATION,
                str(current_user_id),
                str(time.time())
            )
            # create download directory, if not exist
            if not os.path.isdir(new_download_location):
                os.makedirs(new_download_location)
            await message.edit_text("trying to download")
            # try to download the "link"
            sagtus, err_message = await call_apropriate_function(
                aria_i_p,
                dl_url,
                new_download_location,
                message,
                is_zip
            )
            if not sagtus:
                # if FAILED, display the error message
                await message.edit_text(err_message)


async def ytdl_btn_k(message: Message):
    i_m_sefg = await message.edit_text("processing")
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = await extract_link(
        message.reply_to_message, "YTDL"
    )
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.reply_to_message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            # cf_name,
            yt_dl_user_name,
            yt_dl_pass_word,
            user_working_dir
        )
        await i_m_sefg.edit_text(
            text=text_message,
            reply_markup=reply_markup
        )
    else:
        await i_m_sefg.delete()
