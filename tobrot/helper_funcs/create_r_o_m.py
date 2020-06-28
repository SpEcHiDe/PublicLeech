#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

import configparser

from pyrogram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from tobrot import (
    R_CLONE_CONF_URI
)
from tobrot.helper_funcs.r_clone import (
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
    if R_CLONE_CONF_URI is not None:
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
