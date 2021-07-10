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

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

import configparser

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from publicleechgroup import (
    R_CLONE_CONF_URI
)
from publicleechgroup.helper_funcs.r_clone import (
    get_r_clone_config
)


async def get_markup(message: Message):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton(
        "leech 🤔🤔",
        callback_data=("leech").encode("UTF-8")
    ))
    ikeyboard.append(InlineKeyboardButton(
        "youtube-dl",
        callback_data=("ytdl").encode("UTF-8")
    ))
    inline_keyboard.append(ikeyboard)
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton(
        "A leech TAR . GZ  🤔🤔",
        callback_data=("leecha").encode("UTF-8")
    ))
    ikeyboard.append(InlineKeyboardButton(
        "A youtube-dl TAR . GZ",
        callback_data=("ytdla").encode("UTF-8")
    ))
    inline_keyboard.append(ikeyboard)
    ikeyboard = []
    if R_CLONE_CONF_URI:
        r_clone_conf_file = await get_r_clone_config(
            R_CLONE_CONF_URI,
            message._client
        )
        if r_clone_conf_file is not None:
            config = configparser.ConfigParser()
            config.read(r_clone_conf_file)
            remote_names = config.sections()
            it_r = 0
            for remote_name in remote_names:
                ikeyboard.append(InlineKeyboardButton(
                    f"RClone LEECH {remote_name}",
                    callback_data=(f"leech_rc_{it_r}").encode("UTF-8")
                ))
                # ikeyboard.append(InlineKeyboardButton(
                #     f"RClone YTDL {remote_name}",
                #     callback_data=(f"ytdl_rc_{it_r}").encode("UTF-8")
                # ))
                inline_keyboard.append(ikeyboard)
                ikeyboard = []
                it_r = it_r + 1
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    inline_keyboard = []

    reply_text = (
        "please select the required option"
    )
    return reply_text, reply_markup
