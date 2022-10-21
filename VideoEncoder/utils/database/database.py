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

import datetime

import motor.motor_asyncio


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.col2 = self.db.status

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            extensions='MP4',
            hevc=False,
            aspect=False,
            cabac=False,
            reframe='pass',
            tune=True,
            frame='source',
            audio='aac',
            sample='source',
            bitrate='source',
            bits=False,
            channels='source',
            drive=False,
            preset='sf',
            metadata=True,
            hardsub=False,
            watermark=False,
            subtitles=True,
            resolution='OG',
            upload_as_doc=False,
            crf=22,
            resize=False
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    # Telegram Related

    # Upload As Doc
    async def set_upload_as_doc(self, id, upload_as_doc):
        await self.col.update_one({'id': id}, {'$set': {'upload_as_doc': upload_as_doc}})

    async def get_upload_as_doc(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('upload_as_doc', False)

    # Encoding Settings

    # Resize
    async def set_resize(self, id, resize):
        await self.col.update_one({'id': id}, {'$set': {'resize': resize}})

    async def get_resize(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('resize', 'resize')

    # Frame
    async def set_frame(self, id, frame):
        await self.col.update_one({'id': id}, {'$set': {'frame': frame}})

    async def get_frame(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('frame', 'source')

    # Convert To 720p
    async def set_resolution(self, id, resolution):
        await self.col.update_one({'id': id}, {'$set': {'resolution': resolution}})

    async def get_resolution(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('resolution', 'OG')

    # Video Bits
    async def set_bits(self, id, bits):
        await self.col.update_one({'id': id}, {'$set': {'bits': bits}})

    async def get_bits(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bits', False)

    # Copy Subtitles
    async def set_subtitles(self, id, subtitles):
        await self.col.update_one({'id': id}, {'$set': {'subtitles': subtitles}})

    async def get_subtitles(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('subtitles', False)

    # Sample rate
    async def set_samplerate(self, id, sample):
        await self.col.update_one({'id': id}, {'$set': {'sample': sample}})

    async def get_samplerate(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('sample', '44.1K')

    # Extensions
    async def set_extensions(self, id, extensions):
        await self.col.update_one({'id': id}, {'$set': {'extensions': extensions}})

    async def get_extensions(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('extensions', 'MP4')

    # Bit rate
    async def set_bitrate(self, id, bitrate):
        await self.col.update_one({'id': id}, {'$set': {'bitrate': bitrate}})

    async def get_bitrate(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('bitrate', '128')

    # Reframe
    async def set_reframe(self, id, reframe):
        await self.col.update_one({'id': id}, {'$set': {'reframe': reframe}})

    async def get_reframe(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('reframe', 'pass')

    # Audio Codec
    async def set_audio(self, id, audio):
        await self.col.update_one({'id': id}, {'$set': {'audio': audio}})

    async def get_audio(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('audio', 'dd')

    # Audio Channels
    async def set_channels(self, id, channels):
        await self.col.update_one({'id': id}, {'$set': {'channels': channels}})

    async def get_channels(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('channels', 'source')

    # Metadata Watermark
    async def set_metadata_w(self, id, metadata):
        await self.col.update_one({'id': id}, {'$set': {'metadata': metadata}})

    async def get_metadata_w(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('metadata', False)

    # Watermark
    async def set_watermark(self, id, watermark):
        await self.col.update_one({'id': id}, {'$set': {'watermark': watermark}})

    async def get_watermark(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('watermark', False)

    # Preset
    async def set_preset(self, id, preset):
        await self.col.update_one({'id': id}, {'$set': {'preset': preset}})

    async def get_preset(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('preset', 'sf')

    # Hard Sub
    async def set_hardsub(self, id, hardsub):
        await self.col.update_one({'id': id}, {'$set': {'hardsub': hardsub}})

    async def get_hardsub(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('hardsub', False)

    # HEVC
    async def set_hevc(self, id, hevc):
        await self.col.update_one({'id': id}, {'$set': {'hevc': hevc}})

    async def get_hevc(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('hevc', False)

    # Tune
    async def set_tune(self, id, tune):
        await self.col.update_one({'id': id}, {'$set': {'tune': tune}})

    async def get_tune(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('tune', False)

    # CABAC
    async def set_cabac(self, id, cabac):
        await self.col.update_one({'id': id}, {'$set': {'cabac': cabac}})

    async def get_cabac(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('cabac', False)

    # Aspect ratio
    async def set_aspect(self, id, aspect):
        await self.col.update_one({'id': id}, {'$set': {'aspect': aspect}})

    async def get_aspect(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('aspect', False)

    # Google Drive
    async def set_drive(self, id, drive):
        await self.col.update_one({'id': id}, {'$set': {'drive': drive}})

    async def get_drive(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('drive', False)

    # CRF
    async def get_crf(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('crf', 18)

    async def set_crf(self, id, crf):
        await self.col.update_one({'id': id}, {'$set': {'crf': crf}})

    # Process killed status
    async def get_killed_status(self):
        status = await self.col2.find_one({'id': 'killed'})
        if not status:
            await self.col2.insert_one({'id': 'killed', 'status': False})
            return False
        else:
            return status.get('status')

    async def set_killed_status(self, status):
        await self.col2.update_one({'id': 'killed'}, {'$set': {'status': status}})

    # Auth Chat
    async def get_chat(self):
        status = await self.col2.find_one({'id': 'auth'})
        if not status:
            await self.col2.insert_one({'id': 'auth', 'chat': '5217257368'})
            return '5217257368'
        else:
            return status.get('chat')

    async def set_chat(self, chat):
        await self.col2.update_one({'id': 'auth'}, {'$set': {'chat': chat}})

    # Auth Sudo
    async def get_sudo(self):
        status = await self.col2.find_one({'id': 'sudo'})
        if not status:
            await self.col2.insert_one({'id': 'sudo', 'sudo_': '5217257368'})
            return '5217257368'
        else:
            return status.get('sudo_')

    async def set_sudo(self, sudo):
        await self.col2.update_one({'id': 'sudo'}, {'$set': {'sudo_': sudo}})
