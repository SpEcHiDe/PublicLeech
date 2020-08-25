#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)


def message_filter_f(flt, c: Client, m: Message):
    return bool(
            (
                # below checks the TORRENT detection part
                m.document and
                m.document.file_name.upper().endswith(".TORRENT")
            ) or
            # below checks if it is a valid link
            (
                (
                    ("http" in m.text) or
                    ("magnet:" in m.text)
                ) and (
                    # to avoid conflicts with
                    # popular @LinkToFilesBot (s)
                    ".html" not in m.text
                    )
            )
        )


message_fliter = filters.create(
    func=message_filter_f,
    name="TstMesgFilter"
)
