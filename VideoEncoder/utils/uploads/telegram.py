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
import time

from ... import app, download_dir, log
from ..database.access_db import db
from ..display_progress import progress_for_pyrogram
from ..ffmpeg import get_duration, get_thumbnail, get_width_height


async def upload_to_tg(new_file, message, msg):
    # Variables
    c_time = time.time()
    filename = os.path.basename(new_file)
    duration = get_duration(new_file)
    thumb = get_thumbnail(new_file, download_dir, duration / 4)
    width, height = get_width_height(new_file)
    # Handle Upload
    if await db.get_upload_as_doc(message.from_user.id) is True:
        link = await upload_doc(message, msg, c_time, filename, new_file)
    else:
        link = await upload_video(message, msg, new_file, filename,
                                  c_time, thumb, duration, width, height)
    return link


async def upload_video(message, msg, new_file, filename, c_time, thumb, duration, width, height):
    resp = await message.reply_video(
        new_file,
        supports_streaming=True,
        parse_mode=None,
        caption=filename,
        thumb=thumb,
        duration=duration,
        width=width,
        height=height,
        progress=progress_for_pyrogram,
        progress_args=("Uploading ...", msg, c_time)
    )
    if resp:
        await app.send_video(log, resp.video.file_id, thumb=thumb,
                             caption=filename, duration=duration,
                             width=width, height=height, parse_mode=None)

    return resp.link


async def upload_doc(message, msg, c_time, filename, new_file):
    resp = await message.reply_document(
        new_file,
        caption=filename,
        progress=progress_for_pyrogram,
        progress_args=("Uploading ...", msg, c_time)
    )

    if resp:
        await app.send_document(log, resp.document.file_id, caption=filename, parse_mode=None)

    return resp.link
