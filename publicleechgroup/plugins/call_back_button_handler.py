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

from pyrogram.types import CallbackQuery
from publicleechgroup.amocmadin import Loilacaztion
from publicleechgroup.helper_funcs.youtube_dl_button import youtube_dl_call_back
from publicleechgroup.helper_funcs.icntaosrtsba import (
    leech_btn_k,
    ytdl_btn_k
)


async def button(bot, update: CallbackQuery):
    LOGGER.info(update)
    if not update.message.reply_to_message:
        await update.answer(
            text=Loilacaztion.TGD_YTLD_STOOPID_DRUSER,
            show_alert=True
        )
        return

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
