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
    TG_BOT_TOKEN,
    DIS_ABLE_ST_GFC_COMMAND_I
)
from pyrogram import (
    Client,
    filters
)
from pyrogram.handlers import (
    MessageHandler,
    CallbackQueryHandler
)
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
    eval_message_f,
    upload_document_f,
    save_rclone_conf_f,
    upload_log_file
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
        ":memory:",
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
        filters=filters.command([Commandi.PURGE]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_purge_message_handler)

    # STATUS command
    status_message_handler = MessageHandler(
        status_message_f,
        filters=filters.command([Commandi.STATUS]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(status_message_handler)

    # CANCEL command
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=filters.command([Commandi.CANCEL]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(cancel_message_handler)

    if not SHOULD_USE_BUTTONS:
        LOGGER.info("using COMMANDi mode")
        # LEECH command
        incoming_message_handler = MessageHandler(
            leech_commandi_f,
            filters=filters.command([Commandi.LEECH]) & filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(incoming_message_handler)
    
        # YTDL command
        incoming_youtube_dl_handler = MessageHandler(
            incoming_youtube_dl_f,
            filters=filters.command([Commandi.YTDL]) & filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(incoming_youtube_dl_handler)
    else:
        LOGGER.info("using BUTTONS mode")
        # all messages filter
        # in the AUTH_CHANNELs
        incoming_message_handler = MessageHandler(
            incoming_message_f,
            filters=message_fliter & filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(incoming_message_handler)

    # button is LEGACY command to handle
    # the OLD YTDL buttons,
    # and also the new SUB buttons
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)

    if DIS_ABLE_ST_GFC_COMMAND_I:
        exec_message_handler = MessageHandler(
            exec_message_f,
            filters=filters.command([Commandi.EXEC]) & filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(exec_message_handler)

        eval_message_handler = MessageHandler(
            eval_message_f,
            filters=filters.command([Commandi.EVAL]) & filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(eval_message_handler)

        # MEMEs COMMANDs
        upload_document_handler = MessageHandler(
            upload_document_f,
            filters=filters.command([Commandi.UPLOAD]) & filters.chat(chats=AUTH_CHANNEL)
        )
        app.add_handler(upload_document_handler)

    # HELP command
    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command([Commandi.HELP]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(help_text_handler)

    # not AUTH CHANNEL users
    new_join_handler = MessageHandler(
        new_join_f,
        filters=~filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)

    # welcome MESSAGE
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=filters.chat(chats=AUTH_CHANNEL) & filters.new_chat_members
    )
    app.add_handler(group_new_join_handler)

    # savethumbnail COMMAND
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command([Commandi.SAVETHUMBNAIL]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_thumb_nail_handler)

    # clearthumbnail COMMAND
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command([Commandi.CLEARTHUMBNAIL]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(clear_thumb_nail_handler)

    # an probably easy way to get RClone CONF URI
    save_rclone_conf_handler = MessageHandler(
        save_rclone_conf_f,
        filters=filters.command([Commandi.GET_RCLONE_CONF_URI]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_rclone_conf_handler)

    # Telegram command to upload LOG files
    upload_log_f_handler = MessageHandler(
        upload_log_file,
        filters=filters.command([Commandi.UPLOAD_LOG_FILE]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(upload_log_f_handler)

    # run the APPlication
    app.run()
