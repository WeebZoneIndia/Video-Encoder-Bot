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
from .. import sudo_users, data
from .start import reply_markup
from ..utils.tasks import handle_task

video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]


@Client.on_message(filters.incoming & (filters.video | filters.document))
async def encode_video(app, message):
    user_id = message.from_user.id
    if user_id in sudo_users:
        pass
    else:
        text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>,\nI can encode telegram files in x264 but unfourtunately you have to deploy one for yourself."
        message.reply(text=text, reply_markup=reply_markup)
        return
    if message.document:
        if not message.document.mime_type in video_mimetype:
            return
    await message.reply_text("<code>Added to queue...</code>")
    data.append(message)
    if len(data) == 1:
        await handle_task(message)
