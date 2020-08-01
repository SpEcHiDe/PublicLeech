#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


from tobrot.amocmadin import Loilacaztion


async def new_join_f(client, message):
    # delete all other messages, except for AUTH_CHANNEL
    await message.delete(revoke=True)
    # reply the correct CHAT ID,
    # and LEAVE the chat
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(
            Loilacaztion.WRONG_MESSAGE.format(
                CHAT_ID=message.chat.id
            )
        )
        # leave chat
        await message.chat.leave()


async def help_message_f(client, message):
    # display the /help message
    await message.reply_text(
        Loilacaztion.HELP_MESSAGE,
        quote=True
    )
