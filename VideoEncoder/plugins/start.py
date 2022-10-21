# VideoEncoder - a telegram bot for compressing/encoding videos in h264/h265 format.
# Copyright (c) 2021 WeebTime/VideoEncoder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import shutil
import time
from os import execl as osexecl
from subprocess import run as srun
from sys import executable
from time import time

from psutil import (boot_time, cpu_count, cpu_percent, disk_usage,
                    net_io_counters, swap_memory, virtual_memory)
from pyrogram import Client, filters
from pyrogram.types import Message

from .. import botStartTime, download_dir, encode_dir
from ..utils.database.access_db import db
from ..utils.database.add_user import AddUserToDatabase
from ..utils.display_progress import TimeFormatter, humanbytes
from ..utils.helper import check_chat, start_but

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def uptime():
    """ returns uptime """
    return TimeFormatter(time.time() - botStartTime)


@Client.on_message(filters.command('start'))
async def start_message(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    text = f"Hi {message.from_user.mention()}<a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>!</a> I'm VideoEncoder Bot which will do magic with your file."
    await message.reply(text=text, reply_markup=start_but)


@Client.on_message(filters.command('help'))
async def help_message(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    msg = """<b>📕 Commands List</b>:

- Autodetect Telegram File.
- /ddl - encode through DDL
- /batch - encode in batch
- /queue - check queue
- /settings - settings
- /vset - view settings
- /reset - reset settings
- /stats - cpu stats

For Sudo:
- /exec - Execute Python
- /sh - Execute Shell
- /vupload - video upload
- /dupload - doc upload
- /gupload - drive upload
- /update - git pull
- /restart - restart bot
- /clean - clean junk
- /clear - clean queue
- /logs - view logs

For Owner:
- /addchat and /addsudo
- /rmsudo and /rmchat

Supports: <a href='https://telegra.ph/Supports-03-29'>click here</a>"""
    await message.reply(text=msg, disable_web_page_preview=True, reply_markup=start_but)


@Client.on_message(filters.command('stats'))
async def show_status_count(_, event: Message):
    c = await check_chat(event, chat='Both')
    if not c:
        return
    await AddUserToDatabase(_, event)
    text = await show_status(_)
    await event.reply_text(text)


async def show_status(_):
    currentTime = TimeFormatter(time() - botStartTime)
    osUptime = TimeFormatter(time() - boot_time())
    total, used, free, disk = disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    memory = virtual_memory()
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    total_users = await db.total_users_count()
    text = f"""<b>Uptime of</b>:
- <b>Bot:</b> {currentTime}
- <b>OS:</b> {osUptime}

<b>Disk</b>:
<b>- Total:</b> {total}
<b>- Used:</b> {used}
<b>- Free:</b> {free}

<b>UL:</b> {sent} | <b>DL:</b> {recv}
<b>CPU:</b> {cpuUsage}%

<b>Cores:</b>
<b>- Physical:</b> {p_core}
<b>- Total:</b> {t_core}
<b>- Used:</b> {swap_p}%

<b>RAM:</b> 
- <b>Total:</b> {mem_t}
- <b>Free:</b> {mem_a}
- <b>Used:</b> {mem_u}

Users: {total_users}"""
    return text


async def showw_status(_):
    currentTime = TimeFormatter(time() - botStartTime)
    total, used, free, disk = disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpuUsage = cpu_percent(interval=0.5)
    total_users = await db.total_users_count()

    text = f"""Uptime of Bot: {currentTime}

Disk:
- Total: {total}
- Used: {used}
- Free: {free}
CPU: {cpuUsage}%

Users: {total_users}"""
    return text


@Client.on_message(filters.command('clean'))
async def delete_files(_, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    delete_downloads()
    await message.reply_text('Deleted all junk files!')


def delete_downloads():
    dir = encode_dir
    dir2 = download_dir
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    for files in os.listdir(dir2):
        path = os.path.join(dir2, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


@Client.on_message(filters.command('restart'))
async def font_message(app, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    await AddUserToDatabase(app, message)
    reply = await message.reply_text('Restarting...')
    textx = f"Done Restart...✅"
    await reply.edit_text(textx)
    try:
        exit()
    finally:
        osexecl(executable, executable, "-m", "VideoEncoder")


@Client.on_message(filters.command('update'))
async def update_message(app, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    await AddUserToDatabase(app, message)
    reply = await message.reply_text('📶 Fetching Update...')
    textx = f"✅ Bot Updated"
    await reply.edit_text(textx)
    try:
        await app.stop()
    finally:
        srun([f"bash run.sh"], shell=True)
