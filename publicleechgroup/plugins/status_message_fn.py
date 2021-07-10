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
import io
import os
import shutil
import sys
import time
import traceback
from publicleechgroup import (
    BOT_START_TIME,
    LOGGER,
    LOG_FILE_ZZGEVC,
    MAX_MESSAGE_LENGTH
)
from publicleechgroup.helper_funcs.download_aria_p_n import (
    aria_start
)
from publicleechgroup.helper_funcs.upload_to_tg import upload_to_tg
from publicleechgroup.dinmamoc import Commandi
from publicleechgroup.amocmadin import Loilacaztion
from publicleechgroup.helper_funcs.display_progress import (
    time_formatter,
    humanbytes
)


async def status_message_f(client, message):
    aria_i_p = await aria_start()
    # Show All Downloads
    downloads = aria_i_p.get_downloads()
    #
    DOWNLOAD_ICON = "📥"
    UPLOAD_ICON = "📤"
    #
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
        msg += f"<u>{downloading_dir_name}</u>"
        msg += " | "
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
        msg += f"<code>{Commandi.CANCEL} {current_gid}</code>"
        msg += " | "
        msg += "\n\n"
    LOGGER.info(msg)

    if msg == "":
        msg = Loilacaztion.NO_TOR_STATUS

    currentTime = time_formatter((time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    ms_g = f"<b>Bot Uptime</b>: <code>{currentTime}</code>\n" \
        f"<b>Total disk space</b>: <code>{total}</code>\n" \
        f"<b>Used</b>: <code>{used}</code>\n" \
        f"<b>Free</b>: <code>{free}</code>\n"

    msg = ms_g + "\n" + msg
    await message.reply_text(msg, quote=True)


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        # /cancel command
        i_m_s_e_g = await message.reply_text(
            Loilacaztion.PROCESSING,
            quote=True
        )
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            downloads = aria_i_p.get_download(g_id)
            LOGGER.info(downloads)
            LOGGER.info(downloads.remove(force=True, files=True))
            await i_m_s_e_g.edit_text(
                Loilacaztion.TOR_CANCELLED
            )
        except Exception as e:
            LOGGER.warn(str(e))
            await i_m_s_e_g.edit_text(
                Loilacaztion.TOR_CANCEL_FAILED
            )
    else:
        await message.delete()


async def exec_message_f(client, message):
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "😐"
    o = stdout.decode()
    if not o:
        o = "😐"
    return_code = process.returncode
    OUTPUT = ""
    OUTPUT += "<b>EXEC</b>:\n"
    OUTPUT += "<u>Command</u>\n"
    OUTPUT += f"<code>{cmd}</code>\n"
    OUTPUT += f"<u>PID</u>: <code>{process.pid}</code>\n\n"
    OUTPUT += "<b>stderr:</b>\n"
    OUTPUT += f"<code>{e}</code>\n\n"
    OUTPUT += "<b>stdout:</b>\n"
    OUTPUT += f"<code>{o}</code>\n\n"
    OUTPUT += f"<b>return</b>: <code>{return_code}</code>"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await client.send_document(
            chat_id=message.chat.id,
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("exec.text")
        await message.delete()
    else:
        await message.reply_text(OUTPUT)


async def upload_document_f(client, message):
    imsegd = await message.reply_text(
        Loilacaztion.PROCESSING
    )
    if " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        recvd_response = await upload_to_tg(
            imsegd,
            local_file_name,
            message.from_user.id,
            {}
        )
        LOGGER.info(recvd_response)
    await imsegd.delete()


async def save_rclone_conf_f(client, message):
    chat_type = message.chat.type
    r_clone_conf_uri = None
    if chat_type in ["private", "bot", "group"]:
        r_clone_conf_uri = f"https://t.me/PublicLeech/{message.chat.id}/{message.reply_to_message.message_id}"
    elif chat_type in ["supergroup", "channel"]:
        if message.chat.username:
            r_clone_conf_uri = "please DO NOT upload confidential credentials, in a public group."
        else:
            r_clone_conf_uri = f"https://t.me/c/{str(message.reply_to_message.chat.id)[4:]}/{message.reply_to_message.message_id}"
    else:
        r_clone_conf_uri = "unknown chat_type"
    await message.reply_text(
        "<code>"
        f"{r_clone_conf_uri}"
        "</code>"
    )


async def upload_log_file(client, message):
    await message.reply_document(
        LOG_FILE_ZZGEVC
    )


async def eval_message_f(client, message):
    ismgese = await message.reply_text("...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc.strip()
    elif stderr:
        evaluation = stderr.strip()
    elif stdout:
        evaluation = stdout.strip()
    else:
        evaluation = "😐"

    final_output = ""
    final_output += f"<b>EVAL</b>: <code>{cmd}</code>"
    final_output += "\n\n<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation}</code>\n"

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await ismgese.reply_document(
            document="eval.text",
            caption=cmd
        )
        os.remove("eval.text")
        await ismgese.delete()
    else:
        await ismgese.edit(final_output)


async def aexec(code, client, message):
    exec(
        f'async def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)
