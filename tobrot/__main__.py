#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


import os

from tobrot import (
    APP_ID,
    API_HASH,
    AUTH_CHANNEL,
    DOWNLOAD_LOCATION,
    LOGGER,
    SHOULD_USE_BUTTONS,
    TG_BOT_TOKEN
)

from pyrogram import Client, Filters, MessageHandler, CallbackQueryHandler

from tobrot.plugins.new_join_fn import (
    new_join_f,
    help_message_f
)
from tobrot.plugins.incoming_message_fn import (
    incoming_message_f,
    incoming_youtube_dl_f,
    incoming_purge_message_f,
    leech_commandi_f
)
from tobrot.plugins.status_message_fn import (
    status_message_f,
    cancel_message_f,
    exec_message_f,
    upload_document_f,
    save_rclone_conf_f
)
from tobrot.plugins.call_back_button_handler import button
from tobrot.plugins.custom_thumbnail import (
    save_thumb_nail,
    clear_thumb_nail
)
from tobrot.helper_funcs.custom_filters import message_fliter
from tobrot.dinmamoc import Commandi


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    app = Client(
        "LeechBot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        workers=343,
        workdir=DOWNLOAD_LOCATION
    )
    #
    app.set_parse_mode("html")
    #
    # PURGE command
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=Filters.command([PURGE@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_purge_message_handler)

    # STATUS command
    status_message_handler = MessageHandler(
        status_message_f,
        filters=Filters.command([STATUS@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(status_message_handler)

    # CANCEL command
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=Filters.command([CANCEL@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(cancel_message_handler)

    if not SHOULD_USE_BUTTONS:
        LOGGER.info("using COMMANDi mode")
        # LEECH command
        incoming_message_handler = MessageHandler(
            leech_commandi_f,
            filters=Filters.command([LEECH@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(incoming_message_handler)
    
        # YTDL command
        incoming_youtube_dl_handler = MessageHandler(
            incoming_youtube_dl_f,
            filters=Filters.command([YTDL@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(incoming_youtube_dl_handler)
    else:
        LOGGER.info("using BUTTONS mode")
        # all messages filter
        # in the AUTH_CHANNELs
        incoming_message_handler = MessageHandler(
            incoming_message_f,
            filters=message_fliter & Filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(incoming_message_handler)

    # button is LEGACY command to handle
    # the OLD YTDL buttons,
    # and also the new SUB buttons
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)

    #
    # MEMEs COMMANDs
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=Filters.command([EXEC@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(exec_message_handler)

    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=Filters.command([UPLOAD@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(upload_document_handler)

    # HELP command
    help_text_handler = MessageHandler(
        help_message_f,
        filters=Filters.command([HELP@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(help_text_handler)

    # not AUTH CHANNEL users
    new_join_handler = MessageHandler(
        new_join_f,
        filters=~Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)

    # welcome MESSAGE
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=Filters.chat(chats=AUTH_CHANNEL) & Filters.new_chat_members
    )
    app.add_handler(group_new_join_handler)

    # savethumbnail COMMAND
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=Filters.command([SAVETHUMBNAIL@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_thumb_nail_handler)

    # clearthumbnail COMMAND
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=Filters.command([CLEARTHUMBNAIL@Publicleechrobot]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(clear_thumb_nail_handler)

    # an probably easy way to get RClone CONF URI
    save_rclone_conf_handler = MessageHandler(
        save_rclone_conf_f,
        filters=Filters.command([@Publicleechrobot.GET_RCLONE_CONF_URI]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_rclone_conf_handler)

    # run the APPlication
    app.run()
