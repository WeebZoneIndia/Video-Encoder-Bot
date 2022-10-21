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
import json
import os

from pyrogram import Client
from pyrogram.types import CallbackQuery

from .. import app, download_dir, log, owner, sudo_users
from ..plugins.queue import queue_answer
from ..utils.database.access_db import db
from ..utils.settings import (AudioSettings, ExtraSettings, OpenSettings,
                              VideoSettings)
from .start import showw_status


@app.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    # Close Button

    if "closeMeh" in cb.data:
        await cb.message.delete(True)

    # Settings

    elif "VideoSettings" in cb.data:
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    elif "OpenSettings" in cb.data:
        await OpenSettings(cb.message, user_id=cb.from_user.id)

    elif "AudioSettings" in cb.data:
        await AudioSettings(cb.message, user_id=cb.from_user.id)

    elif "ExtraSettings" in cb.data:
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    elif "triggerMode" in cb.data:
        if await db.get_drive(cb.from_user.id) is True:
            await db.set_drive(cb.from_user.id, drive=False)
        else:
            await db.set_drive(cb.from_user.id, drive=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    elif "triggerUploadMode" in cb.data:
        if await db.get_upload_as_doc(cb.from_user.id) is True:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    elif "triggerResize" in cb.data:
        if await db.get_resize(cb.from_user.id) is True:
            await db.set_resize(cb.from_user.id, resize=False)
        else:
            await db.set_resize(cb.from_user.id, resize=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    # Watermark
    elif "Watermark" in cb.data:
        await cb.answer("Sir, this button not works XD\n\nPress Bottom Buttons.", show_alert=True)

    # Metadata
    elif "triggerMetadata" in cb.data:
        if await db.get_metadata_w(cb.from_user.id):
            await db.set_metadata_w(cb.from_user.id, metadata=False)
        else:
            await db.set_metadata_w(cb.from_user.id, metadata=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    # Watermark
    elif "triggerVideo" in cb.data:
        if await db.get_watermark(cb.from_user.id):
            await db.set_watermark(cb.from_user.id, watermark=False)
        else:
            await db.set_watermark(cb.from_user.id, watermark=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    # Subtitles
    elif "triggerHardsub" in cb.data:
        if await db.get_hardsub(cb.from_user.id):
            await db.set_hardsub(cb.from_user.id, hardsub=False)
        else:
            await db.set_hardsub(cb.from_user.id, hardsub=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    elif "triggerSubtitles" in cb.data:
        if await db.get_subtitles(cb.from_user.id):
            await db.set_subtitles(cb.from_user.id, subtitles=False)
        else:
            await db.set_subtitles(cb.from_user.id, subtitles=True)
        await ExtraSettings(cb.message, user_id=cb.from_user.id)

    # Extension
    elif "triggerextensions" in cb.data:
        ex = await db.get_extensions(cb.from_user.id)
        if ex == 'MP4':
            await db.set_extensions(cb.from_user.id, extensions='MKV')
        elif ex == 'MKV':
            await db.set_extensions(cb.from_user.id, extensions='AVI')
        else:
            await db.set_extensions(cb.from_user.id, extensions='MP4')
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Frame
    elif "triggerframe" in cb.data:
        fr = await db.get_frame(cb.from_user.id)
        if fr == 'ntsc':
            await db.set_frame(cb.from_user.id, frame='source')
        elif fr == 'source':
            await db.set_frame(cb.from_user.id, frame='pal')
        elif fr == 'pal':
            await db.set_frame(cb.from_user.id, frame='film')
        elif fr == 'film':
            await db.set_frame(cb.from_user.id, frame='23.976')
        elif fr == '23.976':
            await db.set_frame(cb.from_user.id, frame='30')
        elif fr == '30':
            await db.set_frame(cb.from_user.id, frame='60')
        else:
            await db.set_frame(cb.from_user.id, frame='ntsc')
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Preset
    elif "triggerPreset" in cb.data:
        p = await db.get_preset(cb.from_user.id)
        if p == 'uf':
            await db.set_preset(cb.from_user.id, preset='sf')
        elif p == 'sf':
            await db.set_preset(cb.from_user.id, preset='vf')
        elif p == 'vf':
            await db.set_preset(cb.from_user.id, preset='f')
        elif p == 'f':
            await db.set_preset(cb.from_user.id, preset='m')
        elif p == 'm':
            await db.set_preset(cb.from_user.id, preset='s')
        else:
            await db.set_preset(cb.from_user.id, preset='uf')
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # sample rate
    elif "triggersamplerate" in cb.data:
        sr = await db.get_samplerate(cb.from_user.id)
        if sr == '44.1K':
            await db.set_samplerate(cb.from_user.id, sample='48K')
        elif sr == '48K':
            await db.set_samplerate(cb.from_user.id, sample='source')
        else:
            await db.set_samplerate(cb.from_user.id, sample='44.1K')
        await AudioSettings(cb.message, user_id=cb.from_user.id)

    # bitrate
    elif "triggerbitrate" in cb.data:
        bit = await db.get_bitrate(cb.from_user.id)
        if bit == '400':
            await db.set_bitrate(cb.from_user.id, bitrate='320')
        elif bit == '320':
            await db.set_bitrate(cb.from_user.id, bitrate='256')
        elif bit == '256':
            await db.set_bitrate(cb.from_user.id, bitrate='224')
        elif bit == '224':
            await db.set_bitrate(cb.from_user.id, bitrate='192')
        elif bit == '192':
            await db.set_bitrate(cb.from_user.id, bitrate='160')
        elif bit == '160':
            await db.set_bitrate(cb.from_user.id, bitrate='128')
        elif bit == '128':
            await db.set_bitrate(cb.from_user.id, bitrate='source')
        else:
            await db.set_bitrate(cb.from_user.id, bitrate='400')
        await AudioSettings(cb.message, user_id=cb.from_user.id)

    # Audio Codec
    elif "triggerAudioCodec" in cb.data:
        a = await db.get_audio(cb.from_user.id)
        if a == 'dd':
            await db.set_audio(cb.from_user.id, audio='copy')
        elif a == 'copy':
            await db.set_audio(cb.from_user.id, audio='aac')
        elif a == 'aac':
            await db.set_audio(cb.from_user.id, audio='opus')
        elif a == 'opus':
            await db.set_audio(cb.from_user.id, audio='alac')
        elif a == 'alac':
            await db.set_audio(cb.from_user.id, audio='vorbis')
        else:
            await db.set_audio(cb.from_user.id, audio='dd')
        await AudioSettings(cb.message, user_id=cb.from_user.id)

    # Audio Channel
    elif "triggerAudioChannels" in cb.data:
        c = await db.get_channels(cb.from_user.id)
        if c == 'source':
            await db.set_channels(cb.from_user.id, channels='1.0')
        elif c == '1.0':
            await db.set_channels(cb.from_user.id, channels='2.0')
        elif c == '2.0':
            await db.set_channels(cb.from_user.id, channels='2.1')
        elif c == '2.1':
            await db.set_channels(cb.from_user.id, channels='5.1')
        elif c == '5.1':
            await cb.answer("7.1 is for bluray only.", show_alert=True)
            await db.set_channels(cb.from_user.id, channels='7.1')
        else:
            await db.set_channels(cb.from_user.id, channels='source')
        await AudioSettings(cb.message, user_id=cb.from_user.id)

    # Resolution
    elif "triggerResolution" in cb.data:
        r = await db.get_resolution(cb.from_user.id)
        if r == 'OG':
            await db.set_resolution(cb.from_user.id, resolution='1080')
        elif r == '1080':
            await db.set_resolution(cb.from_user.id, resolution='720')
        elif r == '720':
            await db.set_resolution(cb.from_user.id, resolution='480')
        elif r == '480':
            await db.set_resolution(cb.from_user.id, resolution='576')
        else:
            await db.set_resolution(cb.from_user.id, resolution='OG')
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Video Bits
    elif "triggerBits" in cb.data:
        b = await db.get_bits(cb.from_user.id)
        if await db.get_hevc(cb.from_user.id):
            if b:
                await db.set_bits(cb.from_user.id, bits=False)
            else:
                await db.set_bits(cb.from_user.id, bits=True)
        else:
            if b:
                await db.set_bits(cb.from_user.id, bits=False)
            else:
                await cb.answer("H264 don't support 10 bits in this bot.",
                                show_alert=True)
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # HEVC
    elif "triggerHevc" in cb.data:
        if await db.get_hevc(cb.from_user.id):
            await db.set_hevc(cb.from_user.id, hevc=False)
        else:
            await db.set_hevc(cb.from_user.id, hevc=True)
            await cb.answer("H265 need more time for encoding video", show_alert=True)
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Tune
    elif "triggertune" in cb.data:
        if await db.get_tune(cb.from_user.id):
            await db.set_tune(cb.from_user.id, tune=False)
        else:
            await db.set_tune(cb.from_user.id, tune=True)
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Reframe
    elif "triggerreframe" in cb.data:
        rf = await db.get_reframe(cb.from_user.id)
        if rf == '4':
            await db.set_reframe(cb.from_user.id, reframe='8')
        elif rf == '8':
            await db.set_reframe(cb.from_user.id, reframe='16')
            await cb.answer("Reframe 16 maybe not support", show_alert=True)
        elif rf == '16':
            await db.set_reframe(cb.from_user.id, reframe='pass')
        else:
            await db.set_reframe(cb.from_user.id, reframe='4')
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # CABAC
    elif "triggercabac" in cb.data:
        if await db.get_cabac(cb.from_user.id):
            await db.set_cabac(cb.from_user.id, cabac=False)
        else:
            await db.set_cabac(cb.from_user.id, cabac=True)
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Aspect
    elif "triggeraspect" in cb.data:
        if await db.get_aspect(cb.from_user.id):
            await db.set_aspect(cb.from_user.id, aspect=False)
        else:
            await db.set_aspect(cb.from_user.id, aspect=True)
            await cb.answer("This will help to force video to 16:9", show_alert=True)
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    elif "triggerCRF" in cb.data:
        crf = await db.get_crf(cb.from_user.id)
        nextcrf = int(crf) + 1
        if nextcrf > 30:
            await db.set_crf(cb.from_user.id, crf=18)
        else:
            await db.set_crf(cb.from_user.id, crf=nextcrf)
        await VideoSettings(cb.message, user_id=cb.from_user.id)

    # Cancel

    elif "cancel" in cb.data:
        status = download_dir + "status.json"
        with open(status, 'r+') as f:
            statusMsg = json.load(f)
            user = cb.from_user.id
            if user != statusMsg['user']:
                if user == 885190545:
                    pass
                elif user in sudo_users or user in owner:
                    pass
                else:
                    return
            statusMsg['running'] = False
            f.seek(0)
            json.dump(statusMsg, f, indent=2)
            os.remove('VideoEncoder/utils/extras/downloads/process.txt')
            try:
                await cb.message.edit_text("🚦🚦 Process Cancelled 🚦🚦")
                chat_id = log
                utc_now = datetime.datetime.utcnow()
                ist_now = utc_now + \
                    datetime.timedelta(minutes=30, hours=5)
                ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
                bst_now = utc_now + \
                    datetime.timedelta(minutes=00, hours=6)
                bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
                now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                await bot.send_message(chat_id, f"**Last Process Cancelled, Bot is Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            except:
                pass

    # Stats
    elif 'stats' in cb.data:
        stats = await showw_status(bot)
        stats = stats.replace('<b>', '')
        stats = stats.replace('</b>', '')
        await cb.answer(stats, show_alert=True)

    # Queue
    elif "queue+" in cb.data:
        await queue_answer(app, cb)
