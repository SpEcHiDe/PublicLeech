#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import asyncio
import os
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from tobrot.helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from tobrot.helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from tobrot.helper_funcs.split_large_files import split_large_files
from tobrot.helper_funcs.copy_similar_file import copy_file

from tobrot import (
    TG_MAX_FILE_SIZE,
    EDIT_SLEEP_TIME_OUT,
    DOWNLOAD_LOCATION
)


async def upload_to_tg(
    message,
    local_file_name,
    from_user,
    dict_contatining_uploaded_files
):
    LOGGER.info(local_file_name)
    base_file_name = os.path.basename(local_file_name)
    caption_str = ""
    caption_str += "<code>"
    caption_str += base_file_name
    caption_str += "</code>"
    # caption_str += "\n\n"
    # caption_str += "<a href='tg://user?id="
    # caption_str += str(from_user)
    # caption_str += "'>"
    # caption_str += "Here is the file to the link you sent"
    # caption_str += "</a>"LOGGER.info(directory_contents)
    LOGGER.info(local_file_name)
    LOGGER.info(local_file_name)
    LOGGER.info(local_file_name)
    LOGGER.info(local_file_name)
    LOGGER.info(local_file_name)
    LOGGER.info(" base base base base") 
    LOGGER.info(base_file_name) 
    LOGGER.info(base_file_name) 
    LOGGER.info(base_file_name) 
    LOGGER.info(base_file_name) 
    LOGGER.info(base_file_name) 
    LOGGER.info(base_file_name) 
    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        directory_contents.sort()
        # number_of_files = len(directory_contents)
        LOGGER.info(" loop loop loop loop loop loop loop") 
        LOGGER.info(directory_contents)
        LOGGER.info(directory_contents)
        LOGGER.info(directory_contents)
        LOGGER.info(directory_contents)
        LOGGER.info(directory_contents)
        LOGGER.info(directory_contents)



        new_m_esg = message
        if not message.photo:
            new_m_esg = await message.reply_text(
                "Found {} files".format(len(directory_contents)),
                quote=True
                # reply_to_message_id=message.message_id
            )
        for single_file in directory_contents:
            # recursion: will this FAIL somewhere?
            await upload_to_tg(
                new_m_esg,
                os.path.join(local_file_name, single_file),
                from_user,
                dict_contatining_uploaded_files
            )
    else:
        if os.path.getsize(local_file_name) > TG_MAX_FILE_SIZE:
            LOGGER.info("TODO")
            d_f_s = humanbytes(os.path.getsize(local_file_name))
            i_m_s_g = await message.reply_text(
                "Telegram does not support uploading this file.\n"
                f"Detected File Size: {d_f_s} 😡\n"
                "\n🤖 trying to split the files 🌝🌝🌚"
            )
            splitted_dir = await split_large_files(local_file_name)
            totlaa_sleif = os.listdir(splitted_dir)
            totlaa_sleif.sort()
            number_of_files = len(totlaa_sleif)
            LOGGER.info(totlaa_sleif)
            ba_se_file_name = os.path.basename(local_file_name)
            await i_m_s_g.edit_text(
                f"Detected File Size: {d_f_s} 😡\n"
                f"<code>{ba_se_file_name}</code> splitted into {number_of_files} files.\n"
                "Trying to upload to Telegram, now ..."
            )
            for le_file in totlaa_sleif:
                # recursion: will this FAIL somewhere?
                await upload_to_tg(
                    message,
                    os.path.join(splitted_dir, le_file),
                    from_user,
                    dict_contatining_uploaded_files
                )
        else:
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user
            )
            if sent_message is not None:
                dict_contatining_uploaded_files[os.path.basename(local_file_name)] = sent_message.message_id
    # await message.delete()
    return dict_contatining_uploaded_files


async def upload_single_file(message, local_file_name, caption_str, from_user):
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    sent_message = None
    start_time = time.time()
    #
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION,
        "thumbnails",
        str(from_user) + ".jpg"
    )
    LOGGER.info(thumbnail_location)
    #
    try:
        message_for_progress_display = message
        if not message.photo:
            message_for_progress_display = await message.reply_text(
                "starting upload of {}".format(os.path.basename(local_file_name))
            )
        if local_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            # if a file, don't upload "thumb"
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            #
            # send document
            qwerty = os.getcwd()
            qwerty = "===========  " + qwerty
            LOGGER.info(qwerty)
            
            dir_pathakc = "============dir_pathakc============" + os.path.dirname(os.path.realpath(__file__))
            LOGGER.info(dir_pathakc)
            
            
            dir_pathakc = "============(os.path.basename(local_file_name)============" + os.path.dirname((os.path.basename(local_file_name))
            LOGGER.info(dir_pathakc)
            
            asdfghjk = "===============AKCFILE = " + local_file_name
            LOGGER.info(asdfghjk)
            sent_message = await message.reply_document(
                document=local_file_name,
                # quote=True,
                thumb=thumb,
                caption=caption_str,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Trying to upload {}".format(os.path.basename(local_file_name)),
                    message_for_progress_display,
                    start_time
                )
            )
            if thumb is not None:
                os.remove(thumb)
        elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send audio
            sent_message = await message.reply_audio(
                audio=local_file_name,
                # quote=True,
                caption=caption_str,
                parse_mode="html",
                duration=duration,
                performer=artist,
                title=title,
                thumb=thumb,
                disable_notification=True,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Trying to upload {}".format(os.path.basename(local_file_name)),
                    message_for_progress_display,
                    start_time
                )
            )
            if thumb is not None:
                os.remove(thumb)
        else:
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            # if a file, don't upload "thumb"
            # this "diff" is a major derp -_- 😔😭😭
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            #
            # send document
            sent_message = await message.reply_document(
                document=local_file_name,
                # quote=True,
                thumb=thumb,
                caption=caption_str,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Trying to upload {}".format(os.path.basename(local_file_name)),
                    message_for_progress_display,
                    start_time
                )
            )
            if thumb is not None:
                os.remove(thumb)
    except Exception as e:
        await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
    else:
        await message_for_progress_display.delete()
    os.remove(local_file_name)
    return sent_message
