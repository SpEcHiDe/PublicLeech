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

import asyncio
from publicleechgroup.helper_funcs.display_progress import humanbytes
import json
import os
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from publicleechgroup import (
    LOGGER,
    DEF_THUMB_NAIL_VID_S
)


async def extract_youtube_dl_formats(url, yt_dl_user_name, yt_dl_pass_word, user_working_dir):
    command_to_exec = [
        "youtube-dl",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url
    ]
    if "hotstar" in url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")
    #
    if yt_dl_user_name is not None:
        command_to_exec.append("--username")
        command_to_exec.append(yt_dl_user_name)
    if yt_dl_pass_word is not None:
        command_to_exec.append("--password")
        command_to_exec.append(yt_dl_pass_word)

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
    # LOGGER.info(e_response)
    t_response = stdout.decode().strip()
    # LOGGER.info(t_response)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    if e_response:
        # logger.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace(
            "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", ""
        )
        return None, error_message, None
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
        response_json = []
        if "\n" in x_reponse:
            for yu_r in x_reponse.split("\n"):
                response_json.append(json.loads(yu_r))
        else:
            response_json.append(json.loads(x_reponse))
        # response_json = json.loads(x_reponse)
        save_ytdl_json_path = user_working_dir + \
            "/" + str("ytdleech") + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        # logger.info(response_json)
        inline_keyboard = []
        #
        thumb_image = DEF_THUMB_NAIL_VID_S
        #
        for current_r_json in response_json:
            # LOGGER.info(current_r_json)
            #
            thumb_image = current_r_json.get("thumbnails", None)
            # LOGGER.info(thumb_image)
            if thumb_image is not None:
                # YouTube acts weirdly,
                # and not in the same way as Telegram
                thumb_image = thumb_image[-1]["url"]
            if thumb_image is None:
                thumb_image = DEF_THUMB_NAIL_VID_S

            duration = None
            if "duration" in current_r_json:
                duration = current_r_json["duration"]
            if "formats" in current_r_json:
                for formats in current_r_json["formats"]:
                    format_id = formats.get("format_id")
                    format_string = formats.get("format_note")
                    if format_string is None:
                        format_string = formats.get("format")
                    # don't display formats, without audio
                    # https://t.me/c/1434259219/269937
                    if "DASH" in format_string.upper():
                        continue
                    format_ext = formats.get("ext")
                    approx_file_size = ""
                    if "filesize" in formats:
                        approx_file_size = humanbytes(formats["filesize"])
                    n_ue_sc = bool("video only" in format_string)
                    scneu = "DL" if not n_ue_sc else "XM"
                    dipslay_str_uon = " " + format_string + " (" + format_ext.upper() + ") " + approx_file_size + " "
                    cb_string_video = "{}|{}|{}|{}".format(
                        "video", format_id, format_ext, scneu
                    )
                    ikeyboard = []
                    if "drive.google.com" in url:
                        if format_id == "source":
                            ikeyboard = [
                                InlineKeyboardButton(
                                    dipslay_str_uon,
                                    callback_data=(cb_string_video).encode("UTF-8")
                                )
                            ]
                    else:
                        if format_string is not None and not "audio only" in format_string:
                            ikeyboard = [
                                InlineKeyboardButton(
                                    dipslay_str_uon,
                                    callback_data=(cb_string_video).encode("UTF-8")
                                )
                            ]
                        else:
                            # special weird case :\
                            ikeyboard = [
                                InlineKeyboardButton(
                                    "SVideo [" +
                                    "] ( " +
                                    approx_file_size + " )",
                                    callback_data=(cb_string_video).encode("UTF-8")
                                )
                            ]
                    inline_keyboard.append(ikeyboard)
                if duration is not None:
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "MP3 (64 kbps)", callback_data="audio|64k|mp3|_"),
                        InlineKeyboardButton(
                            "MP3 (128 kbps)", callback_data="audio|128k|mp3|_")
                    ])
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "MP3 (320 kbps)", callback_data="audio|320k|mp3|_")
                    ])
            else:
                format_id = current_r_json["format_id"]
                format_ext = current_r_json["ext"]
                cb_string_video = "{}|{}|{}|{}".format(
                    "video", format_id, format_ext, "DL"
                )
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "SVideo",
                        callback_data=(cb_string_video).encode("UTF-8")
                    )
                ])
            # TODO: :\
            break
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        # LOGGER.info(reply_markup)
        succss_mesg = (
            "Select the desired format: 👇\n"
            "<u>mentioned</u> <i>file size might be approximate</i>"
        )
        return thumb_image, succss_mesg, reply_markup
