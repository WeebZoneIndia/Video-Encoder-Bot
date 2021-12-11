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

from pyrogram import Client, filters

from .. import (audio, crf, doc_thumb, preset, resolution, sudo_users, tune,
                upload_doc)
from ..utils.utils import check_user, output, start


@Client.on_message(filters.command('start'))
async def start_message(app, message):
    check = await check_user(message)
    if check is None:
        return
    text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>. I can encode telegram files in x264.\n\nPress /help for my commands :)"
    await message.reply(text=text, reply_markup=start)


@Client.on_message(filters.command('help'))
async def help_message(app, message):
    check = await check_user(message)
    if check is None:
        return
    text = f"""<b>Commands:</b>
• AutoDetect Telegram Files.
• /help - Commands List.
• /start - Introduction.
• /vset - View Settings.
• /sthumb - Save Thumb
• /dthumb - Clear Thumb.
• /logs - check logs."""
    await message.reply(text=text, reply_markup=output)


@Client.on_message(filters.command('vset'))
async def vset(app, message):
    check = await check_user(message)
    if check is None:
        return
    text = f'''<b>Encode Settings</b>
Tune: <code>{tune}</code> | <code>Preset: {preset}</code>
Audio: <code>{audio} | <code>CRF: {crf}</code>
Resolution: <code>{resolution}</code>

<b>Upload Settings<b>
Upload Mode: <code>{'Document' if (upload_doc) else 'Video' }</code>
Doc thumb: <code>{'True' if (doc_thumb) else 'False'}</code>

<b>Sudo Users</b>
<code>{sudo_users}</code>
'''
    await message.reply(text=text, reply_markup=start)


@Client.on_message(filters.command('logs'))
async def logs(app, message):
    check = await check_user(message)
    if check is None:
        return
    file = 'VideoEncoder/utils/logs.txt'
    await message.reply_document(file, caption='#Logs')
