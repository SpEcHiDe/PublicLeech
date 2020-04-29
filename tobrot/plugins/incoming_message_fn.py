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


import os

from tobrot import (
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT
)


import aria2p
import time
import asyncio
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function, aria_start
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats

async def incoming_statuz_message_f(client, message):
    """/statuz command"""
    if await AdminCheck(client, message.chat.id, message.from_user.id):

        #
        DOWNLOAD_ICON = "📥"
        UPLOAD_ICON = "📤"
        #
        
        msg_statuz = await message.reply_text("Current Status 😎", quote=True)
        prev_msg = ""
        akccounter = 1
        exitakc = 0
        
        aria_i_p = await aria_start()
        
        while 1:        
            # Show All Downloads
            downloads = aria_i_p.get_downloads()
            
            msg = ""
            for download in downloads:
                downloading_dir_name = "NA"
                try:
                    downloading_dir_name = str(download.name)
                except:
                    pass
                total_length_size = str(download.total_length_string())
                progress_percent_string = str(download.progress_string())
                down_speed_string = str(download.download_speed_string())
                up_speed_string = str(download.upload_speed_string())
                download_current_status = str(download.status)
                e_t_a = str(download.eta_string())
                current_gid = str(download.gid)
                #
                msg += f"<u><code>{downloading_dir_name}</code></u>"
                msg += "\n| "
                msg += f"{total_length_size}"
                msg += " | "
                msg += f"{progress_percent_string}"
                msg += " | "
                msg += f"{DOWNLOAD_ICON} {down_speed_string}"
                msg += " | "
                msg += f"{UPLOAD_ICON} {up_speed_string}"
                msg += " | "
                msg += f"{e_t_a}"
                msg += " | "
                msg += f"{download_current_status}"
                msg += " | "
                msg += f"\n<code>/cancel {current_gid}</code>"
                msg += " | "
                msg += "\n\n"
                if exitakc == 1:
                    msg += "**Over & Out** 🔊"
            LOGGER.info(msg)
            if msg == "":
                msg = "🤷‍♂️ No Active, Queued or Paused TORRENTs"
                
            if akccounter == 1:
                #msg_statuz2 = await msg_statuz.reply_text(msg, quote=True)
                await msg_statuz.edit(msg)
            else:
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            #await msg_statuz.delete()
                LOGGER.info("=======================")
                LOGGER.info(msg_statuz)
                LOGGER.info(msg)
                LOGGER.info("=======================")
                await msg_statuz.edit(msg)
                
            if exitakc == 1:
                break;
            if prev_msg == msg:
                #await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                #msg += "\n**Over & Out** 🔊"
                #LOGGER.info("=======================")
                #LOGGER.info(msg_statuz)
                #LOGGER.info(msg)
                #LOGGER.info("=======================")
                #await msg_statuz.delete()
                #await message.reply_text(msg, quote=True)
                exitakc = 1
            prev_msg = msg
            akccounter = akccounter + 1

        
async def incoming_purge_message_f(client, message):
    """/purge command"""
    i_m_sefg2 = await message.reply_text("Purging...", quote=True)
    if await AdminCheck(client, message.chat.id, message.from_user.id):
        aria_i_p = await aria_start()
        # Show All Downloads
        downloads = aria_i_p.get_downloads()
        for download in downloads:
            LOGGER.info(download.remove(force=True))
    await i_m_sefg2.delete()

async def incoming_message_f(client, message):
    """/leech command"""
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    if len(message.command) > 1:
        if message.command[1] == "archive":
            is_zip = True
    # get link from the incoming message
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        akcm = dl_url.split('\n')
        for akc_url in akcm:
            await i_m_sefg.edit_text("extracting links")
            # start the aria2c daemon
            aria_i_p = await aria_start()
            LOGGER.info(aria_i_p)
            current_user_id = message.from_user.id
            # create an unique directory
            new_download_location = os.path.join(
                DOWNLOAD_LOCATION,
                str(current_user_id),
                str(time.time())
            )
            # create download directory, if not exist
            if not os.path.isdir(new_download_location):
                os.makedirs(new_download_location)
            await i_m_sefg.edit_text("trying to download")
            # try to download the "link"
            sagtus, err_message = await call_apropriate_function(
                aria_i_p,
                akc_url,
                new_download_location,
                i_m_sefg,
                is_zip
            )
            if not sagtus:
                # if FAILED, display the error message
                await i_m_sefg.edit_text(err_message)
    else:
        await i_m_sefg.edit_text("**ERR**! What have you entered. Please read /help")


def extract_link_split(message):
    url = message.text
    return url



async def incoming_split_message_f(client, message):
    """/splitmag command"""
    dl_url = extract_link_split(message.reply_to_message)
    LOGGER.info(dl_url)
    akcm = dl_url.split('\n')
    msgbkp = message
    i_m_sefg = []
    for akci in range(len(akcm)):
        i_m_sefg.append(await msgbkp.reply_text(akcm[akci], quote=True))
        await i_m_sefg[akci].reply_text("/leech @TorSeed2eubot", quote=True)
        
async def incoming_youtube_dl_f(client, message):
    """ /ytdl command """
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            user_working_dir
        )
        if thumb_image is not None:
            await message.reply_photo(
                photo=thumb_image,
                quote=True,
                caption=text_message,
                reply_markup=reply_markup
            )
            await i_m_sefg.delete()
        else:
            await i_m_sefg.edit_text(
                text=text_message,
                reply_markup=reply_markup
            )
    else:
        # if no links found, delete the "processing" message
        await i_m_sefg.delete()
