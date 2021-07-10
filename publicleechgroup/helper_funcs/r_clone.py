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

import os
import re
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
from publicleechgroup.helper_funcs.run_shell_command import run_command


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
    t_response, e_response = await run_command(command_to_exec)
    # Wait for the subprocess to finish
    LOGGER.info(e_response)
    LOGGER.info(t_response)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    remote_file_id = await r_clone_extract_link_s(
        re.escape(src),
        remote_name,
        remote_dir,
        conf_file
    )
    LOGGER.info(remote_file_id)
    return remote_file_id


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


async def r_clone_extract_link_s(
    src_file_name: str,
    remote_name: str,
    remote_dir: str,
    conf_file: str
):
    tmp_file_name = "lsf_filter.txt"
    with open(tmp_file_name, "w+", encoding="utf-8") as f_d:
        f_d.write(f"+ {src_file_name}\n- *")
    command_to_exec = [
        "rclone",
        "lsf",
        "-F",
        "-i",
        f"--filter-from={tmp_file_name}",
        "--files-only",
        "" + remote_name + ":" + remote_dir + "",
        "--config=" + conf_file + ""
    ]
    LOGGER.info(command_to_exec)
    t_response, e_response = await run_command(command_to_exec)
    # Wait for the subprocess to finish
    LOGGER.info(e_response)
    LOGGER.info(t_response)
    os.remove(tmp_file_name)
    return t_response
