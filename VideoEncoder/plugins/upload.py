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

import html
import os
import time

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid

from .. import download_dir, sudo_users
from ..utils.ffmpeg import get_duration, get_thumbnail, get_width_height
from ..utils.helper import check_chat
from ..utils.uploads.drive.upload import Uploader
from ..utils.uploads.telegram import upload_doc, upload_video


@Client.on_message(filters.command('dupload'))
async def docupload(client, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    c_time = time.time()
    file = os.path.expanduser(' '.join(message.command[1:]))
    if not file:
        await message.reply('you forgot to mention path!')
        return
    text = f'Uploading {html.escape(file)}...'
    reply = await message.reply(text)
    filename = os.path.basename(file)

    try:
        await upload_doc(message, reply, c_time, filename, file)
    except Exception as e:
        await reply.edit('Error while uploading! {}'.format(e))
    else:
        await reply.delete()


@Client.on_message(filters.command('vupload'))
async def videoupload(client, message):
    c = await check_chat(message, chat='Sudo')
    if c is None:
        return
    c_time = time.time()
    file = os.path.expanduser(' '.join(message.command[1:]))
    if not file:
        await message.reply_text('you forgot to mention filepath!')
        return
    filename = os.path.basename(file)
    duration = get_duration(file)
    thumb = get_thumbnail(file, download_dir, duration / 4)
    width, height = get_width_height(file)
    text = f'Uploading {html.escape(file)}...'
    reply = await message.reply_text(text)
    try:
        await upload_video(message, reply, file, filename,
                           c_time, thumb, duration, width, height)
    except Exception as e:
        await reply.edit('Error while uploading! {}'.format(e))
    else:
        await reply.delete()


@Client.on_message(filters.command('gupload'))
async def driveupload(client, message):
    c = await check_chat(message, chat='Sudo')
    if c is None:
        return
    new_file = os.path.expanduser(' '.join(message.command[1:]))
    if not new_file:
        await message.reply_text('you forgot to mention path!')
        return
    text = f'Uploading {html.escape(new_file)}...'
    reply = await message.reply_text(text)
    try:
        u = Uploader()
        await u.upload_to_drive(new_file, message, reply)
    except:
        await reply.edit('Error while uploading!')
    else:
        await reply.delete()


@Client.on_message(filters.command('logs'))
async def logsup(client, message):
    c = await check_chat(message, chat='Sudo')
    if c is None:
        return
    file = 'VideoEncoder/utils/extras/logs.txt'
    caption = '#Logs'
    try:
        await message.reply_document(
            file,
            caption=caption
        )
    except MessageIdInvalid:
        await message.reply('Upload cancelled!')
    except Exception as e:
        await message.reply(': {}'.format(e))
