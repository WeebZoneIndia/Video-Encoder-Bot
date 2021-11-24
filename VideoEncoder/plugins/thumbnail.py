# VideoEncoder - a telegram bot for compressing/encoding videos in h264 format.
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

# Code Taken from github.com/WeebTime/Torrent-Bot-Lazyleech/blob/Master/lazyleech/utils/misc.py

import os
import tempfile

from pyrogram import Client, filters

from .. import download_dir
from ..utils.utils import check_user, convert_to_jpg, get_file_mimetype


@Client.on_message(filters.command('sthumb'))
async def savethumbnail(client, message):
    check = await check_user(message)
    if check is None:
        return
    else:
        pass
    reply = message.reply_to_message
    document = message.document
    photo = message.photo
    thumbset = False
    user_id = message.from_user.id
    thumbnail_path = os.path.join(str(user_id), 'thumbnail.jpg')
    os.makedirs(str(user_id), exist_ok=True)
    if document or photo:
        if photo or (document.file_size < 10485760 and os.path.splitext(document.file_name)[1] and (not document.mime_type or document.mime_type.startswith('image/'))):
            with tempfile.NamedTemporaryFile(dir=str(user_id)) as tempthumb:
                await message.download(tempthumb.name)
                mimetype = await get_file_mimetype(tempthumb.name)
                if mimetype.startswith('image/'):
                    await convert_to_jpg(tempthumb.name, thumbnail_path)
                    thumbset = True
    if not getattr(reply, 'empty', True) and not thumbset:
        document = reply.document
        photo = reply.photo
        if document or photo:
            if photo or (document.file_size < 10485760 and os.path.splitext(document.file_name)[1] and (not document.mime_type or document.mime_type.startswith('image/'))):
                with tempfile.NamedTemporaryFile(dir=str(user_id)) as tempthumb:
                    await reply.download(tempthumb.name)
                    mimetype = await get_file_mimetype(tempthumb.name)
                    if mimetype.startswith('image/'):
                        await convert_to_jpg(tempthumb.name, thumbnail_path)
                        thumbset = True
    if thumbset:
        await message.reply_text('Thumbnail set')
    else:
        await message.reply_text('Cannot find thumbnail')


@Client.on_message(filters.command('dthumb'))
async def rmthumbnail(client, message):
    for path in ('thumbnail'):
        path = os.path.join(str(message.from_user.id), f'{path}.jpg')
        if os.path.isfile(path):
            os.remove(path)
    await message.reply_text('Thumbnail cleared')
