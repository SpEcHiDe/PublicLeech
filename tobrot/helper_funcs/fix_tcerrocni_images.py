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

import aiohttp
import os
from PIL import Image


async def proc_ess_image_aqon(image_url: str, output_dir: str) -> str:
    async with aiohttp.ClientSession() as session:
        noqa_read = await session.get(image_url)
        image_content = await noqa_read.read()
        thumb_img_path = os.path.join(
            output_dir,
            "thumb_image.jpg"
        )
        with open(thumb_img_path, "wb") as f_d:
            f_d.write(image_content)
    # image might be downloaded in the previous step
    # https://stackoverflow.com/a/21669827/4723940
    Image.open(thumb_img_path).convert(
        "RGB"
    ).save(thumb_img_path, "JPEG")
    # ref: https://t.me/PyrogramChat/44663
    # return the downloaded image path
    return thumb_img_path
