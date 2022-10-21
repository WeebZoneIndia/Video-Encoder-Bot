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

import asyncio

from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from .database.access_db import db
from .database.add_user import AddUserToDatabase


# Settings
async def OpenSettings(event: Message, user_id: int):
    try:
        await event.edit(
            text="Settings of the Bot<a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>!</a>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Video", callback_data="VideoSettings"), InlineKeyboardButton(
                        "Audio", callback_data="AudioSettings")],
                    [InlineKeyboardButton("Extras", callback_data="ExtraSettings"), InlineKeyboardButton(
                        "Close", callback_data="closeMeh")]
                ]
            )
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await OpenSettings(event, user_id)
    except MessageNotModified:
        pass


# Video Settings
async def VideoSettings(event: Message, user_id: int):
    try:
        ex = await db.get_extensions(user_id)
        if ex == 'MP4':
            extensions = 'MP4'
        elif ex == 'MKV':
            extensions = 'MKV'
        elif ex == 'AVI':
            extensions = 'AVI'

        fr = await db.get_frame(user_id)
        if fr == 'ntsc':
            frame = 'NTSC'
        elif fr == 'pal':
            frame = 'PAL'
        elif fr == 'film':
            frame = 'FILM'
        elif fr == '23.976':
            frame = '23.976'
        elif fr == '30':
            frame = '30'
        elif fr == '60':
            frame = '60'
        elif fr == 'source':
            frame = 'Source'

        p = await db.get_preset(user_id)
        if p == 'uf':
            pre = 'UltraFast'
        elif p == 'sf':
            pre = 'SuperFast'
        elif p == 'vf':
            pre = 'VeryFast'
        elif p == 'f':
            pre = 'Fast'
        elif p == 'm':
            pre = 'Medium'
        elif p == 's':
            pre = 'Slow'
        else:
            pre = 'None'

        crf = await db.get_crf(user_id)

        r = await db.get_resolution(user_id)
        if r == 'OG':
            res = 'Source'
        elif r == '1080':
            res = '1080p'
        elif r == '720':
            res = '720p'
        elif r == '576':
            res = '576p'
        elif r == '480':
            res = '480p'

        # Reframe
        rf = await db.get_reframe(user_id)
        if rf == '4':
            reframe = '4'
        elif rf == '8':
            reframe = '8'
        elif rf == '16':
            reframe = '16'
        elif rf == 'pass':
            reframe = 'Pass'

        fr = await db.get_frame(user_id)
        if fr == 'ntsc':
            frame = 'NTSC'
        elif fr == 'pal':
            frame = 'PAL'
        elif fr == 'film':
            frame = 'FILM'
        elif fr == '23.976':
            frame = '23.976'
        elif fr == '30':
            frame = '30'
        elif fr == '60':
            frame = '60'
        elif fr == 'source':
            frame = 'Source'

        await event.edit(
            text="Here's Your Video Settings<a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>:</a>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(
                        f"Basic Settings", callback_data="Watermark")],
                    [InlineKeyboardButton(f"Ext: {extensions} ", callback_data="triggerextensions"),
                     InlineKeyboardButton(f"Bits: {'10' if ((await db.get_bits(user_id)) is True) else '8'}", callback_data="triggerBits")],
                    [InlineKeyboardButton(f"Codec: {'H265' if ((await db.get_hevc(user_id)) is True) else 'H264'}", callback_data="triggerHevc"),
                     InlineKeyboardButton(f"CRF: {crf}", callback_data="triggerCRF")],
                    [InlineKeyboardButton(f"Quality", callback_data="Watermark"),
                     InlineKeyboardButton(f"{res}", callback_data="triggerResolution")],
                    [InlineKeyboardButton(f"Tune", callback_data="Watermark"),
                     InlineKeyboardButton(f"{'Animation' if ((await db.get_tune(user_id)) is True) else 'Film'}", callback_data="triggertune")],
                    [InlineKeyboardButton(
                        f"Advanced Settings", callback_data="Watermark")],
                    [InlineKeyboardButton(f"Preset", callback_data="Watermark"),
                     InlineKeyboardButton(f"{pre}", callback_data="triggerPreset")],
                    [InlineKeyboardButton(f"FPS: {frame}", callback_data="triggerframe"),
                     InlineKeyboardButton(f"Aspect: {'16:9' if ((await db.get_aspect(user_id)) is True) else 'Source'}", callback_data="triggeraspect")],
                    [InlineKeyboardButton(f"CABAC {'☑️' if ((await db.get_cabac(user_id)) is True) else ''}", callback_data="triggercabac"),
                     InlineKeyboardButton(f"Reframe: {reframe}", callback_data="triggerreframe")],
                    [InlineKeyboardButton(
                        f"Back", callback_data="OpenSettings")]
                ]
            )
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await VideoSettings(event, user_id)
    except MessageNotModified:
        pass


async def AudioSettings(event: Message, user_id: int):
    try:

        a = await db.get_audio(user_id)
        if a == 'dd':
            audio = 'AC3'
        elif a == 'aac':
            audio = 'AAC'
        elif a == 'opus':
            audio = 'OPUS'
        elif a == 'vorbis':
            audio = 'VORBIS'
        elif a == 'alac':
            audio = 'ALAC'
        elif a == 'copy':
            audio = 'Source'
        else:
            audio = 'None'

        bit = await db.get_bitrate(user_id)
        if bit == '400':
            bitrate = '400k'
        elif bit == '320':
            bitrate = '320k'
        elif bit == '256':
            bitrate = '256k'
        elif bit == '224':
            bitrate = '224k'
        elif bit == '192':
            bitrate = '192k'
        elif bit == '160':
            bitrate = '160k'
        elif bit == '128':
            bitrate = '128k'
        elif bit == 'source':
            bitrate = 'Source'

        sr = await db.get_samplerate(user_id)
        if sr == '44.1K':
            sample = '44.1kHz'
        elif sr == '48K':
            sample = '48kHz'
        elif sr == 'source':
            sample = 'Source'

        c = await db.get_channels(user_id)
        if c == '1.0':
            channels = 'Mono'
        elif c == '2.0':
            channels = 'Stereo'
        elif c == '2.1':
            channels = '2.1'
        elif c == '5.1':
            channels = '5.1'
        elif c == '7.1':
            channels = '7.1'
        elif c == 'source':
            channels = 'Source'

        await event.edit(
            text="Here's Your Audio Settings<a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>:</a>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"Codec", callback_data="Watermark"), InlineKeyboardButton(
                        f"{audio}", callback_data="triggerAudioCodec")],
                    [InlineKeyboardButton(f"Channels", callback_data="Watermark"), InlineKeyboardButton(
                        f"{channels}", callback_data="triggerAudioChannels")],
                    [InlineKeyboardButton(f"Sample Rate", callback_data="Watermark"), InlineKeyboardButton(
                        f"{sample}", callback_data="triggersamplerate")],
                    [InlineKeyboardButton(f"Bitrate", callback_data="Watermark"), InlineKeyboardButton(
                        f"{bitrate}", callback_data="triggerbitrate")],
                    [InlineKeyboardButton(
                        f"Back", callback_data="OpenSettings")]
                ]
            )
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await AudioSettings(event, user_id)
    except MessageNotModified:
        pass


async def ExtraSettings(event: Message, user_id: int):
    try:
        await event.edit(
            text="Here's Your Subtitle Settings<a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>:</a>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(
                        f"Subtitles Settings", callback_data="Watermark")],
                    [InlineKeyboardButton(f"Hardsub {'☑️' if ((await db.get_hardsub(user_id)) is True) else ''}", callback_data="triggerHardsub"), InlineKeyboardButton(f"Copy {'☑️' if ((await db.get_subtitles(user_id)) is True) else ''}", callback_data="triggerSubtitles")],
                    [InlineKeyboardButton(
                        f"Upload Settings", callback_data="Watermark")],
                    [InlineKeyboardButton(f"{'G-Drive' if ((await db.get_drive(user_id)) is True) else 'Telegram'}", callback_data="triggerMode"),
                     InlineKeyboardButton(f"{'Document' if ((await db.get_upload_as_doc(user_id)) is True) else 'Video'}", callback_data="triggerUploadMode")],
                    [InlineKeyboardButton(
                        f"Watermark Settings", callback_data="Watermark")],
                    [InlineKeyboardButton(f"Metadata {'☑️' if ((await db.get_metadata_w(user_id)) is True) else ''}", callback_data="triggerMetadata"), InlineKeyboardButton(f"Video {'☑️' if ((await db.get_watermark(user_id)) is True) else ''}", callback_data="triggerVideo")],
                    [InlineKeyboardButton(
                        f"Back", callback_data="OpenSettings")]
                ]
            )
        )

    except FloodWait as e:
        await asyncio.sleep(e.x)
        await ExtraSettings(event, user_id)
    except MessageNotModified:
        pass
