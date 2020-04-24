#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime

from tobrot import (
    DOWNLOAD_LOCATION,
    AUTH_CHANNEL
)

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.upload_to_tg import upload_to_tg


async def youtube_dl_call_back(bot, update):
    LOGGER.info(update)
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    #
    current_user_id = update.message.reply_to_message.from_user.id
    current_touched_user_id = update.from_user.id
    if current_user_id != current_touched_user_id:
        await bot.answer_callback_query(
            callback_query_id=update.id,
            text="who are you? 🤪🤔🤔🤔",
            show_alert=True,
            cache_time=0
        )
        return False, None
    user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
    # create download directory, if not exist
    if not os.path.isdir(user_working_dir):
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=[
                update.message.message_id,
                update.message.reply_to_message.message_id,
            ],
            revoke=True
        )
        return
    save_ytdl_json_path = user_working_dir + \
        "/" + str("ytdleech") + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
        os.remove(save_ytdl_json_path)
    except (FileNotFoundError) as e:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=[
                update.message.message_id,
                update.message.reply_to_message.message_id,
            ],
            revoke=True
        )
        return False
    #
    response_json = response_json[0]
    # TODO: temporary limitations
    # LOGGER.info(response_json)
    #
    youtube_dl_url = response_json.get("webpage_url")
    LOGGER.info(youtube_dl_url)
    #
    custom_file_name = "%(title)s.%(ext)s"
    # https://superuser.com/a/994060
    LOGGER.info(custom_file_name)
    #
    if "noyes.in" in youtube_dl_url or "tor.checker.in" in youtube_dl_url or "workers.dev" in youtube_dl_url:
        await update.message.edit_caption(
            caption="😡😡 <i>please do not abuse this <u>FREE</u> service</i> 🌚"
        )
        return
    if "drive.google.com" in youtube_dl_url and youtube_dl_format != "source":
        await update.message.edit_caption(
            caption="<i>please do not abuse this <u>FREE</u> service</i>"
        )
        return
    #
    await update.message.edit_caption(
        caption="trying to download"
    )
    description = "@PublicLeech"
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
        # escape Markdown and special characters
    #
    tmp_directory_for_each_user = os.path.join(
        DOWNLOAD_LOCATION,
        str(update.from_user.id)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user
    download_directory = os.path.join(tmp_directory_for_each_user, custom_file_name)
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "youtube-dl",
            "-c",
            "--prefer-ffmpeg",
            "--extract-audio",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory,
            # "--external-downloader", "aria2c"
        ]
    else:
        # command_to_exec = ["youtube-dl", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            for for_mat in response_json["formats"]:
                format_id = for_mat.get("format_id")
                if format_id == youtube_dl_format:
                    acodec = for_mat.get("acodec")
                    vcodec = for_mat.get("vcodec")
                    if acodec == "none" or vcodec == "none":
                        minus_f_format = youtube_dl_format + "+bestaudio"
                    break
        command_to_exec = [
            "youtube-dl",
            "-c",
            "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory,
            # "--external-downloader", "aria2c"
        ]
    #
    command_to_exec.append("--no-warnings")
    # command_to_exec.append("--quiet")
    command_to_exec.append("--restrict-filenames")
    #
    if "hotstar" in youtube_dl_url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")
    LOGGER.info(command_to_exec)
    start = datetime.now()
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    # LOGGER.info(e_response)
    # LOGGER.info(t_response)
    ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await update.message.edit_caption(
            caption=error_message
        )
        return False, None
    if t_response:
        # LOGGER.info(t_response)
        # os.remove(save_ytdl_json_path)
        end_one = datetime.now()
        time_taken_for_download = (end_one -start).seconds
        dir_contents = len(os.listdir(tmp_directory_for_each_user))
        # dir_contents.sort()
        await update.message.edit_caption(
            caption=f"found {dir_contents} files"
        )
        user_id = update.from_user.id
        #
        final_response = await upload_to_tg(
            update.message,
            tmp_directory_for_each_user,
            user_id,
            {}
        )
        LOGGER.info(final_response)
        #
        try:
            shutil.rmtree(tmp_directory_for_each_user)
        except:
            pass
        #
