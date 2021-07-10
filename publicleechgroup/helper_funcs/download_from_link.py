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

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


import asyncio
import time

import os

from publicleechgroup import (
    DOWNLOAD_LOCATION
)


async def request_download(url, file_name, r_user_id):
    directory_path = os.path.join(DOWNLOAD_LOCATION, str(r_user_id), str(time.time()))
    # create download directory, if not exist
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)
    local_file_path = os.path.join(directory_path, file_name)
    command_to_exec = [
        "wget",
        "-O",
        local_file_path,
        url
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    # logger.info(e_response)
    t_response = stdout.decode().strip()
    # logger.info(t_response)
    final_m_r = e_response + "\n\n\n" + t_response
    if os.path.exists(local_file_path):
        return True, local_file_path
    else:
        return False, final_m_r
