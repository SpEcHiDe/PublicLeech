#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  PublicLeech
#  Copyright (C) 2020 The Authors

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

import asyncio
from typing import Union

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

from pyrogram import (
    Client
)
from pyrogram.errors import (
    ChannelInvalid
)


async def copy_via_rclone(
    src: str,
    remote_name: str,
    remote_dir: str,
    conf_file: str
):
    command_to_exec = [
        "rclone",
        "copy",
        src,
        "" + remote_name + ":" + remote_dir + "",
        "--config=" + conf_file + ""
    ]
    LOGGER.info(command_to_exec)
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    LOGGER.info(e_response)
    t_response = stdout.decode().strip()
    LOGGER.info(t_response)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    return None


async def get_r_clone_config(message_link: str, py_client: Client) -> str:
    chat_id, message_id = extract_c_m_ids(message_link)
    try:
        conf_mesg = await py_client.get_messages(
            chat_id=chat_id,
            message_ids=message_id
        )
    except ChannelInvalid:
        LOGGER.info(
            "invalid RClone config URL. this is NOT an ERROR"
        )
        return None
    down_conf_n = await py_client.download_media(
        message=conf_mesg
    )
    return down_conf_n


def extract_c_m_ids(message_link: str) -> (Union[str, int], int):
    p_m_link = message_link.split("/")
    chat_id, message_id = None, None
    if len(p_m_link) == 6:
        # private link
        if p_m_link[3] == "c":
            # the Telegram private link
            chat_id, message_id = int("-100" + p_m_link[4]), int(p_m_link[5])
        elif p_m_link[3] == "PublicLeech":
            # bleck magick
            chat_id, message_id = int(p_m_link[4]), int(p_m_link[5])
    elif len(p_m_link) == 5:
        # public link
        chat_id, message_id = str("@" + p_m_link[3]), int(p_m_link[4])
    return chat_id, message_id
