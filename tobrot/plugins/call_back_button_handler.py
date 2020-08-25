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

from pyrogram.types import CallbackQuery
from tobrot.helper_funcs.youtube_dl_button import youtube_dl_call_back
from tobrot.helper_funcs.icntaosrtsba import (
    leech_btn_k,
    ytdl_btn_k
)


async def button(bot, update: CallbackQuery):
    LOGGER.info(update)
    if update.from_user.id != update.message.reply_to_message.from_user.id:
        return

    await update.answer()
    cb_data = update.data
    
    if cb_data.startswith("leech"):
        await leech_btn_k(update.message, cb_data)

    elif cb_data.startswith("ytdl"):
        await ytdl_btn_k(update.message)

    elif "|" in cb_data:
        await youtube_dl_call_back(bot, update)
