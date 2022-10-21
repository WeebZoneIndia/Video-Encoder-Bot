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

import os.path
import pickle
import re
import urllib.parse as urlparse
from urllib.parse import parse_qs

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
G_DRIVE_FILE_LINK = "https://drive.google.com/open?id={}"
G_DRIVE_FOLDER_LINK = "https://drive.google.com/drive/folders/{}"


def _get_file_id(link: str):
    if "folders" in link or "file" in link:
        regex = r"https://drive\.google\.com/(drive)?/?u?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/([-\w]+)[?+]?/?(w+)?"
        res = re.search(regex, link)
        if res is None:
            return res
        return res.group(5)
    parsed = urlparse.urlparse(link)
    return parse_qs(parsed.query)['id'][0]


class DriveAPI:
    global SCOPES

    # Define the scopes
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self):

        # Variable self.creds will
        # store the user access token.
        # If no valid token found
        # we will create one.
        self.creds = None

        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.

        # Check if file token.pickle exists
        if os.path.exists('token.pickle'):
            # Read the token from the file and
            # store it in the variable self.creds
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available,
        # request the user to log in.
        if not self.creds or not self.creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                self.creds = flow.run_console(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

    def listFolders(self):
        try:
            page_token = None
            folders = []
            while True:
                response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                     spaces='drive',
                                                     fields='nextPageToken, files(id, name)',
                                                     pageToken=page_token).execute()

                for file in response.get('files', []):
                    # Process change
                    folder_data = (file.get('name'), file.get('id'))
                    folders.append(folder_data)

                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            return folders
        except Exception as e:
            print(str(e))
            return None
