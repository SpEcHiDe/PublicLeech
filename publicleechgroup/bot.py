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
import shutil
from publicleechgroup import (
    APP_ID,
    API_HASH,
    AUTH_CHANNEL,
    DOWNLOAD_LOCATION,
    LOGGER,
    SHOULD_USE_BUTTONS,
    TG_BOT_TOKEN,
    DIS_ABLE_ST_GFC_COMMAND_I,
    SLEEP_THRES_HOLD,
    SUDO_USERS
)
from pyrogram import (
    Client,
    filters,
    __version__
)
from pyrogram.handlers import (
    MessageHandler,
    CallbackQueryHandler
)
from publicleechgroup.plugins.new_join_fn import (
    new_join_f,
    help_message_f
)
from publicleechgroup.plugins.incoming_message_fn import (
    incoming_message_f,
    incoming_youtube_dl_f,
    incoming_purge_message_f,
    leech_commandi_f
)
from publicleechgroup.plugins.status_message_fn import (
    status_message_f,
    cancel_message_f,
    exec_message_f,
    eval_message_f,
    upload_document_f,
    save_rclone_conf_f,
    upload_log_file
)
from publicleechgroup.plugins.call_back_button_handler import button
from publicleechgroup.plugins.custom_thumbnail import (
    save_thumb_nail,
    clear_thumb_nail
)
from publicleechgroup.helper_funcs.custom_filters import message_fliter
from publicleechgroup.dinmamoc import Commandi


class Bot(Client):
    """ modded client """
    
    def __init__(self):
        super().__init__(
            ":memory:",
            bot_token=TG_BOT_TOKEN,
            api_id=APP_ID,
            api_hash=API_HASH,
            workers=343,
            workdir=DOWNLOAD_LOCATION,
            parse_mode="html",
            sleep_threshold=SLEEP_THRES_HOLD,
            # TODO: utilize PSP
            # plugins={
            #     "root": "bot/plugins"
            # }
        )

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()

        # create download directory, if not exist
        if not os.path.isdir(DOWNLOAD_LOCATION):
            os.makedirs(DOWNLOAD_LOCATION)
        
        LOGGER(__name__).info(
            "@PublicLeechGroup, trying to add handlers"
        )
        # PURGE command
        self.add_handler(MessageHandler(
            incoming_purge_message_f,
            filters=filters.command(
                [Commandi.PURGE]
            ) & filters.chat(chats=AUTH_CHANNEL)
        ))

        # STATUS command
        self.add_handler(MessageHandler(
            status_message_f,
            filters=filters.command(
                [Commandi.STATUS]
            ) & filters.chat(chats=AUTH_CHANNEL)
        ))

        # CANCEL command
        self.add_handler(MessageHandler(
            cancel_message_f,
            filters=filters.command([Commandi.CANCEL]) & filters.chat(chats=AUTH_CHANNEL)
        ))

        if not SHOULD_USE_BUTTONS:
            LOGGER(__name__).info("using COMMANDi mode")
            # LEECH command
            self.add_handler(MessageHandler(
                leech_commandi_f,
                filters=filters.command(
                    [Commandi.LEECH]
                ) & filters.chat(chats=AUTH_CHANNEL)
            ))
        
            # YTDL command
            self.add_handler(MessageHandler(
                incoming_youtube_dl_f,
                filters=filters.command(
                    [Commandi.YTDL]
                ) & filters.chat(chats=AUTH_CHANNEL)
            ))
        else:
            LOGGER(__name__).info("using BUTTONS mode")
            # all messages filter
            # in the AUTH_CHANNELs
            self.add_handler(MessageHandler(
                incoming_message_f,
                filters=message_fliter & filters.chat(chats=AUTH_CHANNEL)
            ))

        # button is LEGACY command to handle
        # the OLD YTDL buttons,
        # and also the new SUB buttons
        self.add_handler(CallbackQueryHandler(
            button
        ))

        if DIS_ABLE_ST_GFC_COMMAND_I:
            self.add_handler(MessageHandler(
                exec_message_f,
                filters=filters.command([Commandi.EXEC]) & filters.user(users=SUDO_USERS)
            ))

            self.add_handler(MessageHandler(
                eval_message_f,
                filters=filters.command([Commandi.EVAL]) & filters.user(users=SUDO_USERS)
            ))

            # MEMEs COMMANDs
            self.add_handler(MessageHandler(
                upload_document_f,
                filters=filters.command([Commandi.UPLOAD]) & filters.user(users=SUDO_USERS)
            ))

        # HELP command
        self.add_handler(MessageHandler(
            help_message_f,
            filters=filters.command(
                [Commandi.HELP]
            ) & filters.chat(chats=AUTH_CHANNEL)
        ))

        # not AUTH CHANNEL users
        self.add_handler(MessageHandler(
            new_join_f,
            filters=~filters.chat(chats=AUTH_CHANNEL)
        ))

        # welcome MESSAGE
        self.add_handler(MessageHandler(
            help_message_f,
            filters=filters.chat(chats=AUTH_CHANNEL) & filters.new_chat_members
        ))

        # savethumbnail COMMAND
        self.add_handler(MessageHandler(
            save_thumb_nail,
            filters=filters.command(
                [Commandi.SAVETHUMBNAIL]
            ) & filters.chat(chats=AUTH_CHANNEL)
        ))

        # clearthumbnail COMMAND
        self.add_handler(MessageHandler(
            clear_thumb_nail,
            filters=filters.command(
                [Commandi.CLEARTHUMBNAIL]
            ) & filters.chat(chats=AUTH_CHANNEL)
        ))

        # an probably easy way to get RClone CONF URI
        self.add_handler(MessageHandler(
            save_rclone_conf_f,
            filters=filters.command(
                [Commandi.GET_RCLONE_CONF_URI]
            ) & filters.user(users=SUDO_USERS)
        ))

        # Telegram command to upload LOG files
        self.add_handler(MessageHandler(
            upload_log_file,
            filters=filters.command(
                [Commandi.UPLOAD_LOG_FILE]
            ) & filters.user(users=SUDO_USERS)
        ))

        LOGGER(__name__).info(
            f"@{usr_bot_me.username} based on Pyrogram v{__version__} "
        )

    async def stop(self, *args):
        await super().stop()
        shutil.rmtree(
            DOWNLOAD_LOCATION,
            ignore_errors=True
        )
        LOGGER(__name__).info("PublicLeechGroup stopped. Bye.")
