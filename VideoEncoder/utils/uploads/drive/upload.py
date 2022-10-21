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

from __future__ import print_function

import asyncio
import json
import math
import os.path
import time
from mimetypes import MimeTypes

import requests
from googleapiclient.http import MediaFileUpload
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

from .... import app, drive_dir, index, log
from . import DriveAPI
from .download import TimeFormatter, humanbytes, submit_thread


class Uploader(DriveAPI):
    def __init__(self):
        super(Uploader, self).__init__()
        self.__default_depth = 5
        self._output = None
        self._progress = None
        self._is_finished = False

    def finish(self):
        self._is_finished = True

    def uploadFile(self, filePath, parentId):
        try:
            file_name = os.path.basename(filePath)
            mimetype = MimeTypes().guess_type(file_name)[0]

            file_metadata = {'name': file_name}

            if parentId is not None:
                file_metadata["parents"] = [parentId]

            media = MediaFileUpload(filePath,
                                    mimetype=mimetype, chunksize=50*1024*1024,
                                    resumable=True)

            file = self.service.files().create(body=file_metadata,
                                               media_body=media, supportsTeamDrives=True)
            c_time = time.time()
            response = None
            while response is None:
                status, response = file.next_chunk(num_retries=5)
                if status:
                    f_size = status.total_size
                    diff = time.time() - c_time
                    uploaded = status.resumable_progress
                    percentage = uploaded / f_size * 100
                    speed = round(uploaded / diff, 2)
                    eta = round((f_size - uploaded) / speed)
                    text = '<b>Uploading: {}%</b> \n [{}{}] \n • Speed: {}/s \n • Size: {} \n • ETA: {}'
                    self._progress = text.format(
                        round(percentage, 2),
                        "".join(
                            ("█" for _ in range(math.floor(percentage / 10)))),
                        "".join(
                            ("░" for _ in range(10 - math.floor(percentage / 10)))),
                        humanbytes(speed),
                        humanbytes(f_size),
                        TimeFormatter(eta))
                    print(self._progress)
            file_id = response.get('id')
            self._output = self.get_drive_url(filePath, file_id)
        except Exception as e:
            print('[Error]: ' + str(e))
        finally:
            self.finish()

    def get_drive_url(self, filePath, file_id):
        filename = os.path.basename(filePath)
        drive_url = "https://drive.google.com/file/d/" + \
            str(file_id) + "/view?usp=drivesdk"
        if index:
            index_url = requests.utils.requote_uri(f'{index}/{filename}')
            view_url = index_url + '?a=view'
        text = f'{filename}\n\n<a href="{drive_url}">Drive</a> | <a href="{index_url}">Index</a> | <a href="{view_url}">View</a>'
        return str(text)

    async def upload_to_drive(self, new_file, message, msg):
        await msg.edit_text("<code>Uploading...</code>")
        submit_thread(self.uploadFile, new_file, drive_dir)
        while not self._is_finished:
            if self._progress is not None:
                try:
                    await msg.edit(text=self._progress)
                    await asyncio.sleep(4)
                except MessageNotModified:
                    pass
        if self._output:
            ms = await app.send_message(chat_id=message.chat.id, text=self._output)
            await app.send_message(chat_id=log, text=self._output)
        return ms.link
