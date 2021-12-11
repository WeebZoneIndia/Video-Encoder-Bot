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

import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from pyrogram import Client

if os.path.exists('VideoEncoder/config.env'):
    load_dotenv('VideoEncoder/config.env')

### Variables ###

# Basics
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
sudo_users = list(set(int(x)
                  for x in os.environ.get("SUDO_USERS").split()))

# Optional
download_dir = os.environ.get("DOWNLOAD_DIR")
encode_dir = os.environ.get("ENCODE_DIR")
upload_doc = os.environ.get("UPLOAD_AS_DOC")
upload_doc = upload_doc and upload_doc != '0'
doc_thumb = os.environ.get("DOC_THUMB")
doc_thumb = doc_thumb and doc_thumb != '0'

# Encode Settings
resolution = os.environ.get("RESOLUTION")
preset = os.environ.get("PRESET")
tune = os.environ.get("TUNE")
audio = os.environ.get("AUDIO")
crf = os.environ.get("CRF")

SOURCE_MESSAGE = '''
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
'''

data = []

PROGRESS = """
• {0} of {1}
• Speed: {2}
• ETA: {3}
"""


if not os.path.isdir(download_dir):
    os.makedirs(download_dir)

if not os.path.isdir(encode_dir):
    os.makedirs(encode_dir)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            'VideoEncoder/utils/logs.txt',
            backupCount=20
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

app = Client(
    "VideoEncoder",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins={'root': os.path.join(__package__, 'plugins')},
    parse_mode="html",
    sleep_threshold=30)
