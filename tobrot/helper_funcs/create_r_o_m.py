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


from pyrogram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


def get_markup(message: Message):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton(
        "leech 🤔🤔",
        callback_data=("l").encode("UTF-8")
    ))
    ikeyboard.append(InlineKeyboardButton(
        "youtube-dl",
        callback_data=("ytdl").encode("UTF-8")
    ))
    inline_keyboard.append(ikeyboard)
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton(
        "A leech TAR . GZ",
        callback_data=("leecha").encode("UTF-8")
    ))
    ikeyboard.append(InlineKeyboardButton(
        "A youtube-dl TAR . GZ",
        callback_data=("ytdla").encode("UTF-8")
    ))
    inline_keyboard.append(ikeyboard)
    ikeyboard = []

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    inline_keyboard = []

    reply_text = (
        "please select the required option"
    )
    return reply_text, reply_markup
