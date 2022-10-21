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
import io
import math
import os
import time
from concurrent.futures import Future, ThreadPoolExecutor
from signal import SIG_DFL, SIGPIPE, signal
from typing import Any, Callable

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

from .... import download_dir as dir
from ...display_progress import TimeFormatter, humanbytes
from . import G_DRIVE_DIR_MIME_TYPE, DriveAPI, _get_file_id

signal(SIGPIPE, SIG_DFL)


class Downloader(DriveAPI):

    def __init__(self):
        super(Downloader, self).__init__()
        self.DEFAULT_STORAGE_PATH = 'drive_content'
        self._name = ''
        self._completed = 0
        self._list = 1
        self._output = None
        self._progress = None
        self._is_finished = False

    def finish(self):
        self._is_finished = True

    def name(self, file_id):
        drive_file = self.service.files().get(fileId=file_id, supportsTeamDrives=True,
                                              fields="id, name, mimeType, size").execute()
        return drive_file['name']

    def _create_server_dir(self, current_path: str, folder_name: str) -> str:
        path = os.path.join(current_path, folder_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def _list_drive_dir(self, file_id: str):
        query = f"'{file_id}' in parents and (name contains '*')"
        fields = 'nextPageToken, files(id, name, mimeType)'
        page_token = None
        page_size = 100
        files = []
        while True:
            response = self.service.files().list(supportsTeamDrives=True,
                                                 includeTeamDriveItems=True,
                                                 q=query, spaces='drive',
                                                 fields=fields, pageToken=page_token,
                                                 pageSize=page_size, corpora='allDrives',
                                                 orderBy='folder, name').execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    def download(self, file_id: str, name: str):
        try:
            drive_file = self.service.files().get(fileId=file_id, fields="id, name, mimeType",
                                                  supportsTeamDrives=True).execute()
            if drive_file['mimeType'] == G_DRIVE_DIR_MIME_TYPE:
                path = self._create_server_dir(dir, drive_file['name'])
                self.downloadFolder(path, **drive_file)
            else:
                self.downloadFile(dir, **drive_file)
        except Exception as e:
            self._output = 'Download Failed! {}'.format(e)
        finally:
            self.finish()

    def downloadFolder(self, path: str, **kwargs):
        files = self._list_drive_dir(kwargs['id'])
        if len(files) == 0:
            return
        self._list += len(files)
        for file_ in files:
            if file_['mimeType'] == G_DRIVE_DIR_MIME_TYPE:
                path_ = self._create_server_dir(path, file_['name'])
                self.downloadFolder(path_, **file_)
            else:
                self.downloadFile(path, **file_)

    def downloadFile(self, path: str, name: str, **kwargs):
        request = self.service.files().get_media(
            fileId=kwargs['id'], supportsTeamDrives=True)
        fh = io.FileIO(os.path.join(path, name), mode='wb')
        try:
            downloader = MediaIoBaseDownload(
                fh, request, chunksize=50*1024*1024)
            c_time = time.time()
            done = False
            while not done:
                status, done = downloader.next_chunk(num_retries=5)
                if status:
                    downloaded = status.resumable_progress
                    f_size = status.total_size
                    diff = time.time() - c_time
                    progress = downloaded / f_size * 100
                    speed = round(downloaded / diff, 2)
                    eta = round((f_size - downloaded) / speed)
                    text = "Downloading: <code>{}</code>\n[{}{}]\n • Completed: {}\{} • ETA: {}\n • Speed: {}/s  • Size: {}"
                    self._progress = text.format(
                        self._name,
                        "".join(("█"
                                 for _ in range(math.floor(progress / 10)))),
                        "".join(("░"
                                 for _ in range(10 - math.floor(progress / 10)))),
                        self._completed,
                        self._list,
                        TimeFormatter(eta),
                        humanbytes(speed),
                        humanbytes(f_size),)
        except:
            pass
        else:
            self._completed += 1
        finally:
            fh.close()

    async def handle_drive(self, msg, url: str, custom_file_name: str, batch: bool):
        file_id = _get_file_id(url)
        drive_file = self.service.files().get(fileId=file_id, fields="id, name, mimeType",
                                              supportsTeamDrives=True).execute()
        if drive_file['mimeType'] == G_DRIVE_DIR_MIME_TYPE:
            if not batch:
                await msg.edit('use /batch instead.')
                raise IndexError
        self._name = self.name(file_id)
        submit_thread(self.download, file_id, custom_file_name)
        while not self._is_finished:
            if self._progress:
                try:
                    await msg.edit(text=self._progress)
                    await asyncio.sleep(4)
                except MessageNotModified:
                    pass
        if isinstance(self._output, HttpError):
            out = f'[Error]: {self._output._get_reason()}'
            await msg.edit(text=out)
            return None
        return 'Done'


_EXECUTOR = ThreadPoolExecutor(os.cpu_count() + 4)


def submit_thread(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
    """ submit thread to thread pool """
    return _EXECUTOR.submit(func, *args, **kwargs)
