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
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid

from ..utils.utils import check_user, start, output


@Client.on_message(filters.command('start'))
async def start_message(app, message):
    check = await check_user(message)
    if check is None:
        return
    else:
        pass
    text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>. I can encode telegram files in x264.\n\nPress /help for my commands :)"
    await message.reply(text=text, reply_markup=start)


@Client.on_message(filters.command('help'))
async def help_message(app, message):
    check = await check_user(message)
    if check is None:
        return
    else:
        pass
    text = f"""<b>Commands:</b>
• AutoDetect Telegram Files.
• /help - Commands List.
• /start - Introduction.
• /sthumb - Save Thumb
• /dthumb - Clear Thumb.
• /logs - check logs."""
    await message.reply(text=text, reply_markup=output)


@Client.on_message(filters.command('logs'))
async def logs(app, message):
    check = await check_user(message)
    if check is None:
        return
    else:
        pass
    file = 'VideoEncoder/utils/logs.txt'
    await message.reply_document(
        file,
        caption='#Logs'
    )
