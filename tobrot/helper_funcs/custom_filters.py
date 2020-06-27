#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import (
    Filters,
    Message
)


def message_filter_f(f, m: Message):
    return bool(
        m.text or
        m.document.file_name.upper().endswith(".TORRENT")
    )


message_fliter = Filters.create(
    func=message_filter_f,
    name="TstMesgFilter"
)
