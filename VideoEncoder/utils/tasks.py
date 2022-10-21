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
import html
import os
import time
from datetime import datetime
from urllib.parse import unquote_plus

from httpx import delete
from pyrogram.errors.exceptions.bad_request_400 import (MessageIdInvalid,
                                                        MessageNotModified)
from pyrogram.parser import html as pyrogram_html
from pyrogram.types import Message
from requests.utils import unquote

from .. import LOGGER, data, download_dir, video_mimetype
from ..plugins.start import delete_downloads
from .database.access_db import db
from .direct_link_generator import direct_link_generator
from .display_progress import progress_for_pyrogram
from .helper import get_zip_folder, handle_encode, handle_extract, handle_url
from .uploads.drive import _get_file_id
from .uploads.drive.download import Downloader


async def on_task_complete():
    delete_downloads()
    del data[0]
    if not len(data) > 0:
        return
    message = data[0]
    if message.text:
        text = message.text.split(None, 1)
        command = text.pop(0).lower()
        if 'ddl' in command:
            await handle_tasks(message, 'url')
        else:
            await handle_tasks(message, 'batch')
    else:
        if message.document:
            if not message.document.mime_type in video_mimetype:
                return
        await handle_tasks(message, 'tg')


async def handle_tasks(message, mode):
    try:
        msg = await message.reply_text("<b>💠 Downloading...</b>")
        if mode == 'tg':
            await tg_task(message, msg)
        elif mode == 'url':
            await url_task(message, msg)
        else:
            await batch_task(message, msg)
    except MessageNotModified:
        pass
    except IndexError:
        return
    except MessageIdInvalid:
        await msg.edit('Download Cancelled!')
    except FileNotFoundError:
        LOGGER.error('[FileNotFoundError]: Maybe due to cancel, hmm')
    except Exception as e:
        await message.reply(text=f"Error! <code>{e}</code>")
    finally:
        await on_task_complete()


async def tg_task(message, msg):
    filepath = await handle_tg_down(message, msg)
    await msg.edit('Encoding...')
    await handle_encode(filepath, message, msg)


async def url_task(message, msg):
    filepath = await handle_download_url(message, msg, False)
    await msg.edit_text("Encoding...")
    await handle_encode(filepath, message, msg)


async def batch_task(message, msg):
    if message.reply_to_message:
        filepath = await handle_tg_down(message, msg, mode='reply')
    else:
        filepath = await handle_download_url(message, msg, True)
    if not filepath:
        await msg.edit('NO ZIP FOUND!')
    if os.path.isfile(filepath):
        path = await get_zip_folder(filepath)
        await handle_extract(filepath)
        if not os.path.isdir(path):
            await msg.edit('extract failed!')
            return
        filepath = path
    if os.path.isdir(filepath):
        path = filepath
    else:
        await msg.edit('Something went wrong, hell!')
        return
    await msg.edit('<b>📕 Encode Started!</b>')
    sentfiles = []
    # Encode
    for dirpath, subdir, files_ in sorted(os.walk(path)):
        for i in sorted(files_):
            msg_ = await message.reply('Encoding')
            filepath = os.path.join(dirpath, i)
            await msg.edit('Encode Started!\nEncoding: <code>{}</code>'.format(i))
            try:
                url = await handle_encode(filepath, message, msg_)
            except Exception as e:
                await msg_.edit(str(e) + '\n\n Continuing...')
                continue
            else:
                sentfiles.append((i, url))
    text = '✨ <b>#EncodedFiles:</b> \n\n'
    quote = None
    first_index = None
    all_amount = 1
    for filename, filelink in sentfiles:
        if filelink:
            atext = f'- <a href="{filelink}">{html.escape(filename)}</a>'
        else:
            atext = f'- {html.escape(filename)} (empty)'
        atext += '\n'
        futtext = text + atext
        if all_amount > 100:
            thing = await message.reply_text(text, quote=quote, disable_web_page_preview=True)
            if first_index is None:
                first_index = thing
            quote = False
            futtext = atext
            all_amount = 1
            await asyncio.sleep(3)
        all_amount += 1
        text = futtext
    if not sentfiles:
        text = 'Files: None'
    thing = await message.reply_text(text, quote=quote, disable_web_page_preview=True)
    if first_index is None:
        first_index = thing
    await msg.edit('Encoded Files! Links: {}'.format(first_index.link), disable_web_page_preview=True)


async def handle_download_url(message, msg, batch):
    url = message.text.split(None, 1)[1].strip()
    if 'drive.google.com' in url:
        file_id = _get_file_id(url)
        n = Downloader()
        custom_file_name = n.name(file_id)
    else:
        custom_file_name = unquote_plus(os.path.basename(url))
    if "|" in url and not batch:
        url, c_file_name = url.split("|", maxsplit=1)
        url = url.strip()
        if c_file_name:
            custom_file_name = c_file_name.strip()
    direct = direct_link_generator(url)
    if direct:
        url = direct
    path = os.path.join(download_dir, custom_file_name)
    filepath = path
    if 'drive.google.com' in url:
        await n.handle_drive(msg, url, custom_file_name, batch)
    else:
        await handle_url(url, filepath, msg)
    return filepath


async def handle_tg_down(message, msg, mode='no_reply'):
    c_time = time.time()
    if mode == 'no_reply':
        path = await message.download(
            file_name=download_dir,
            progress=progress_for_pyrogram,
            progress_args=("Downloading...", msg, c_time))
    else:
        if message.reply_to_message:
            path = await message.reply_to_message.download(
                file_name=download_dir,
                progress=progress_for_pyrogram,
                progress_args=("Downloading...", msg, c_time))
        else:
            return None
    return path
