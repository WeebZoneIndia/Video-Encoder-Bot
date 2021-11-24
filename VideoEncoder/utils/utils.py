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

import asyncio
import mimetypes

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .. import sudo_users

output = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer", url="https://github.com/WeebTime/"),
     InlineKeyboardButton("Source", url="https://github.com/WeebTime/Video-Encoder-Bot")]
])

start = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer", url="https://github.com/WeebTime/"),
     InlineKeyboardButton("Source", url="https://github.com/WeebTime/Video-Encoder-Bot")],
    [InlineKeyboardButton("Support", url="https://t.me/joinchat/4PQUG5J6aRI3NGQ1"),
     InlineKeyboardButton("Channel", url="https://t.me/WeebZoneIndia")]
])


async def check_user(message):
    try:
        user_id = message.from_user.id
    except AttributeError:
        user_id = message.chat.id
    if user_id in sudo_users:
        return 'Sudo'
    elif user_id == 885190545:
        return 'Dev'
    else:
        text = f"Oops! Not a authorised user, host a video encoder bot for yourself."
        await message.reply(text=text, reply_markup=start)
        return None


async def get_file_mimetype(filename):
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype:
        proc = await asyncio.create_subprocess_exec('file', '--brief', '--mime-type', filename, stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        mimetype = stdout.decode().strip()
    return mimetype or ''

video_duration_cache = dict()
video_duration_lock = asyncio.Lock()


async def convert_to_jpg(original, end):
    proc = await asyncio.create_subprocess_exec('ffmpeg', '-y', '-i', original, end)
    await proc.communicate()
