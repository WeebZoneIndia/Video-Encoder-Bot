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

from ..database.access_db import db
from .drive.upload import Uploader
from .telegram import upload_to_tg


async def upload_worker(new_file, message, msg):
    if await db.get_drive(message.from_user.id):
        link = await Uploader().upload_to_drive(new_file, message, msg)
    else:
        link = await upload_to_tg(new_file, message, msg)
    return link
