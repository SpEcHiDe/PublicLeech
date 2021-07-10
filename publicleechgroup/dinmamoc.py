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

from .get_cfg import get_config


class Commandi:
    LEECH = get_config(
        "COMMANDI_LEECH",
        "leech"
    )
    PURGE = get_config(
        "COMMANDI_PURGE",
        "purge"
    )
    YTDL = get_config(
        "COMMANDI_YTDL",
        "ytdl"
    )
    STATUS = get_config(
        "COMMANDI_STATUS",
        "status"
    )
    CANCEL = get_config(
        "COMMANDI_CANCEL",
        "cancel"
    )
    EXEC = get_config(
        "COMMANDI_EXEC",
        "exec"
    )
    EVAL = get_config(
        "COMMANDI_EVAL",
        "eval"
    )
    RENAME = get_config(
        "COMMANDI_RENAME",
        "rename"
    )
    UPLOAD = get_config(
        "COMMANDI_UPLOAD",
        "upload"
    )
    HELP = get_config(
        "COMMANDI_HELP",
        "help"
    )
    SAVETHUMBNAIL = get_config(
        "COMMANDI_SAVETHUMBNAIL",
        "savethumbnail"
    )
    CLEARTHUMBNAIL = get_config(
        "COMMANDI_CLEARTHUMBNAIL",
        "clearthumbnail"
    )
    GET_RCLONE_CONF_URI = get_config(
        "COMMANDI_GET_RCLONE_CONF_URI",
        "getrcloneconfuri"
    )
    UPLOAD_LOG_FILE = get_config(
        "COMMANDI_UPLOAD_LOG_FILE",
        "log"
    )
