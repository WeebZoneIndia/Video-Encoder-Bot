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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .. import sudo_users

reply_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Support", url="https://t.me/joinchat/4PQUG5J6aRI3NGQ1"),
     InlineKeyboardButton("Channel", url="https://t.me/WeebZoneIndia")],
    [InlineKeyboardButton("Developer", url="https://github.com/WeebTime/"),
     InlineKeyboardButton("Source", url="https://github.com/WeebTime/Video-Encoder-Bot")]
])


@Client.on_message(filters.command(['start', 'help']))
async def start_message(app, message):
    user_id = message.from_user.id
    if user_id in sudo_users:
        text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>,\nI can encode telegram files in x264, just send me a video."
    else:
        text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>,\nI can encode telegram files in x264 but unfourtunately you have to deploy one for yourself."
    await message.reply(text=text, reply_markup=reply_markup)
