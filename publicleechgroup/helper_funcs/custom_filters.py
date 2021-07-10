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
