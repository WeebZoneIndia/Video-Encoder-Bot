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

import asyncio

from pyrogram import Client, filters

from .. import data, video_mimetype
from ..utils.database.add_user import AddUserToDatabase
from ..utils.helper import check_chat
from ..utils.tasks import handle_tasks


@Client.on_message(filters.incoming & (filters.video | filters.document))
async def encode_video(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    if message.document:
        if not message.document.mime_type in video_mimetype:
            return
    data.append(message)
    if len(data) == 1:
        await handle_tasks(message, 'tg')
    else:
        await message.reply("📔 Waiting for queue...")
    await asyncio.sleep(1)


@Client.on_message(filters.command('ddl'))
async def url_encode(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    data.append(message)
    if len(message.text.split()) == 1:
        await message.reply_text("Usage: /ddl [url] | [filename]")
        data.remove(data[0])
        return
    if len(data) == 1:
        await handle_tasks(message, 'url')
    else:
        await message.reply("📔 Waiting for queue...")
    await asyncio.sleep(1)


@Client.on_message(filters.command('batch'))
async def batch_encode(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    data.append(message)
    if len(message.text.split()) == 1:
        await message.reply_text("Usage: /batch [url]")
        data.remove(data[0])
        return
    if len(data) == 1:
        await handle_tasks(message, 'batch')
    else:
        await message.reply("📔 Waiting for queue...")
    await asyncio.sleep(1)
