#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

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
