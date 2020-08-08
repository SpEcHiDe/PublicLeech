#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) PublicLeech Author(s)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tobrot.get_cfg import get_config


class Loilacaztion:
    PROCESSING = get_config(
        "STRINGS_PROCESSING",
        "processing ..."
    )

    CLEARED_THUMBNAIL = get_config(
        "STRINGS_CLEARED_THUMBNAIL",
        "✅ Custom thumbnail cleared succesfully."
    )
    HELP_SAVE_THUMBNAIL = get_config(
        "STRINGS_HELP_SAVE_THUMBNAIL",
        "Reply to a photo to save custom thumbnail"
    )
    SAVED_THUMBNAIL = get_config(
        "STRINGS_SAVED_THUMBNAIL",
        (
            "Custom video / file thumbnail saved. "
            "This image will be used in the upload, till /clearthumbnail."
        )
    )

    HELP_MESSAGE = get_config(
        "STRINGS_HELP_MESSAGE",
        "please read the <a href='https://t.me/c/1434259219/99'>Pinned Message</a>"
    )
    WRONG_MESSAGE = get_config(
        "STRINGS_WRONG_MESSAGE",
        "current CHAT ID: <code>{CHAT_ID}</code>"
    )

    NO_TOR_STATUS = get_config(
        "STRINGS_NO_TOR_STATUS",
        "🤷‍♂️ No Active, Queued or Paused TORRENTs"
    )
    TOR_CANCELLED = get_config(
        "STRINGS_TOR_CANCELLED",
        "Leech Cancelled"
    )
    TOR_CANCEL_FAILED = get_config(
        "STRINGS_TOR_CANCEL_FAILED",
        "<i>FAILED</i>\n\n#error"
    )
