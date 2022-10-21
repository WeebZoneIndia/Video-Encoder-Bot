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
import json
import math
import os
import re
import subprocess
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import ffmpeg

from .. import LOGGER, download_dir, encode_dir
from .database.access_db import db
from .display_progress import TimeFormatter


def get_codec(filepath, channel='v:0'):
    output = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', channel,
                                      '-show_entries', 'stream=codec_name,codec_tag_string', '-of',
                                      'default=nokey=1:noprint_wrappers=1', filepath])
    return output.decode('utf-8').split()


async def extract_subs(filepath, msg, user_id):

    path, extension = os.path.splitext(filepath)
    name = path.split('/')
    check = get_codec(filepath, channel='s:0')
    if check == []:
        return None
    elif check == 'pgs':
        return None
    else:
        output = encode_dir + str(msg.id) + '.ass'
    subprocess.call(['ffmpeg', '-y', '-i', filepath, '-map', 's:0', output])
    subprocess.call(['mkvextract', 'attachments', filepath, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                    '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'])
    subprocess.run([f"mv -f *.JFPROJ *.FNT *.PFA *.ETX *.WOFF *.FOT *.TTF *.SFD *.VLW *.VFB *.PFB *.OTF *.GXF *.WOFF2 *.ODTTF *.BF *.CHR *.TTC *.BDF *.FON *.GF *.PMT *.AMFM  *.MF *.PFM *.COMPOSITEFONT *.PF2 *.GDR *.ABF *.VNF *.PCF *.SFP *.MXF *.DFONT *.UFO *.PFR *.TFM *.GLIF *.XFN *.AFM *.TTE *.XFT *.ACFM *.EOT *.FFIL *.PK *.SUIT *.NFTR *.EUF *.TXF *.CHA *.LWFN *.T65 *.MCF *.YTF *.F3F *.FEA *.SFT *.PFT /usr/share/fonts/"], shell=True)
    subprocess.run([f"mv -f *.jfproj *.fnt *.pfa *.etx *.woff *.fot *.ttf *.sfd *.vlw *.vfb *.pfb *.otf *.gxf *.woff2 *.odttf *.bf *.chr *.ttc *.bdf *.fon *.gf *.pmt *.amfm  *.mf *.pfm *.compositefont *.pf2 *.gdr *.abf *.vnf *.pcf *.sfp *.mxf *.dfont *.ufo *.pfr *.tfm *.glif *.xfn *.afm *.tte *.xft *.acfm *.eot *.ffil *.pk *.suit *.nftr *.euf *.txf *.cha *.lwfn *.t65 *.mcf *.ytf *.f3f *.fea *.sft *.pft /usr/share/fonts/ && fc-cache -f"], shell=True)
    return output


async def encode(filepath, message, msg):

    ex = await db.get_extensions(message.from_user.id)
    path, extension = os.path.splitext(filepath)
    name = path.split('/')

    if ex == 'MP4':
        output_filepathh = encode_dir + name[len(name)-1] + '.mp4'
    elif ex == 'AVI':
        output_filepathh = encode_dir + name[len(name)-1] + '.avi'
    else:
        output_filepathh = encode_dir + name[len(name)-1] + '.mkv'

    output_filepath = output_filepathh
    subtitles_path = encode_dir + str(msg.id) + '.ass'

    progress = download_dir + "process.txt"
    with open(progress, 'w') as f:
        pass

    assert(output_filepath != filepath)

    # Check Path
    if os.path.isfile(output_filepath):
        LOGGER.warning(f'"{output_filepath}": file already exists')
    else:
        LOGGER.info(filepath)

    # HEVC Encode
    x265 = await db.get_hevc(message.from_user.id)
    video_i = get_codec(filepath, channel='v:0')
    if video_i == []:
        codec = ''
    else:
        if x265:
            codec = '-c:v libx265'
        else:
            codec = '-c:v libx264'

    # Tune Encode
    tune = await db.get_tune(message.from_user.id)
    if tune:
        tunevideo = '-tune animation'
    else:
        tunevideo = '-tune film'

    # CABAC
    cbb = await db.get_cabac(message.from_user.id)
    if cbb:
        cabac = '-coder 1'
    else:
        cabac = '-coder 0'

    # Reframe
    rf = await db.get_reframe(message.from_user.id)
    if rf == '4':
        reframe = '-refs 4'
    elif rf == '8':
        reframe = '-refs 8'
    elif rf == '16':
        reframe = '-refs 16'
    else:
        reframe = ''

    # Bits
    b = await db.get_bits(message.from_user.id)
    if not b:
        codec += ' -pix_fmt yuv420p'
    else:
        codec += ' -pix_fmt yuv420p10le'

    # CRF
    crf = await db.get_crf(message.from_user.id)
    if crf:
        Crf = f'-crf {crf}'
    else:
        await db.set_crf(message.from_user.id, crf=26)
        Crf = '-crf 26'

    # Frame
    fr = await db.get_frame(message.from_user.id)
    if fr == 'ntsc':
        frame = '-r ntsc'
    elif fr == 'pal':
        frame = '-r pal'
    elif fr == 'film':
        frame = '-r film'
    elif fr == '23.976':
        frame = '-r 24000/1001'
    elif fr == '30':
        frame = '-r 30'
    elif fr == '60':
        frame = '-r 60'
    else:
        frame = ''

    # Aspect ratio
    ap = await db.get_aspect(message.from_user.id)
    if ap:
        aspect = '-aspect 16:9'
    else:
        aspect = ''

    # Preset
    p = await db.get_preset(message.from_user.id)
    if p == 'uf':
        preset = '-preset ultrafast'
    elif p == 'sf':
        preset = '-preset superfast'
    elif p == 'vf':
        preset = '-preset veryfast'
    elif p == 'f':
        preset = '-preset fast'
    elif p == 'm':
        preset = '-preset medium'
    else:
        preset = '-preset slow'

    # Some Optional Things
    x265 = await db.get_hevc(message.from_user.id)
    if x265:
        video_opts = f'-profile:v main  -map 0:v? -map_chapters 0 -map_metadata 0'
    else:
        video_opts = f'{cabac} {reframe} -profile:v main  -map 0:v? -map_chapters 0 -map_metadata 0'

    # Metadata Watermark
    m = await db.get_metadata_w(message.from_user.id)
    if m:
        metadata = '-metadata title=Weeb-Zone.Blogspot.com -metadata:s:v title=Weeb-Zone.Blogspot.com -metadata:s:a title=Weeb-Zone.Blogspot.com'
    else:
        metadata = ''

    # Copy Subtitles
    h = await db.get_hardsub(message.from_user.id)
    s = await db.get_subtitles(message.from_user.id)
    subs_i = get_codec(filepath, channel='s:0')
    if subs_i == []:
        subtitles = ''
    else:
        if s:
            if h:
                subtitles = ''
            else:
                subtitles = '-c:s copy -c:t copy -map 0:t? -map 0:s?'
        else:
            subtitles = ''


#    ffmpeg_filter = ':'.join([
#        'drawtext=fontfile=/app/bot/utils/watermark/font.ttf',
#        f"text='Weeb-Zone.Blogspot.com'",
#        f'fontcolor=white',
#        'fontsize=main_h/20',
#        f'x=40:y=40'
#    ])

    # Watermark and Resolution
    r = await db.get_resolution(message.from_user.id)
    w = await db.get_watermark(message.from_user.id)
    if r == 'OG':
        watermark = ''
    elif r == '1080':
        watermark = '-vf scale=1920:1080'
    elif r == '720':
        watermark = '-vf scale=1280:720'
    elif r == '576':
        watermark = '-vf scale=768:576'
    else:
        watermark = '-vf scale=852:480'
    if w:
        if r == 'OG':
            watermark += '-vf '
        else:
            watermark += ','
        watermark += 'subtitles=VideoEncoder/utils/extras/watermark.ass'

    # Hard Subs
    if h:
        if r == 'OG':
            if w:
                watermark += ','
            else:
                watermark += '-vf '
        else:
            watermark += ','
        watermark += f'subtitles={subtitles_path}'

    # Sample rate
    sr = await db.get_samplerate(message.from_user.id)
    if sr == '44.1K':
        sample = '-ar 44100'
    elif sr == '48K':
        sample = '-ar 48000'
    else:
        sample = ''

    # bit rate
    bit = await db.get_bitrate(message.from_user.id)
    if bit == '400':
        bitrate = '-b:a 400k'
    elif bit == '320':
        bitrate = '-b:a 320k'
    elif bit == '256':
        bitrate = '-b:a 256k'
    elif bit == '224':
        bitrate = '-b:a 224k'
    elif bit == '192':
        bitrate = '-b:a 192k'
    elif bit == '160':
        bitrate = '-b:a 160k'
    elif bit == '128':
        bitrate = '-b:a 128k'
    else:
        bitrate = ''

    # Audio
    a = await db.get_audio(message.from_user.id)
    a_i = get_codec(filepath, channel='a:0')
    if a_i == []:
        audio_opts = ''
    else:
        if a == 'dd':
            audio_opts = f'-c:a ac3 {sample} {bitrate} -map 0:a?'
        elif a == 'aac':
            audio_opts = f'-c:a aac {sample} {bitrate} -map 0:a?'
        elif a == 'vorbis':
            audio_opts = f'-c:a libvorbis {sample} {bitrate} -map 0:a?'
        elif a == 'alac':
            audio_opts = f'-c:a alac {sample} {bitrate} -map 0:a?'
        elif a == 'opus':
            audio_opts = f'-c:a libopus -vbr on {sample} {bitrate} -map 0:a?'
        else:
            audio_opts = '-c:a copy -map 0:a?'

    # Audio Channel
    c = await db.get_channels(message.from_user.id)
    if c == '1.0':
        channels = '-rematrix_maxval 1.0 -ac 1'
    elif c == '2.0':
        channels = '-rematrix_maxval 1.0 -ac 2'
    elif c == '2.1':
        channels = '-rematrix_maxval 1.0 -ac 3'
    elif c == '5.1':
        channels = '-rematrix_maxval 1.0 -ac 6'
    elif c == '7.1':
        channels = '-rematrix_maxval 1.0 -ac 8'
    else:
        channels = ''

    finish = '-threads 8'

    # Finally
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'quiet',
               '-progress', progress, '-hwaccel', 'auto', '-y', '-i', filepath]
    command.extend((codec.split() + preset.split() + frame.split() + tunevideo.split() + aspect.split() + video_opts.split() + Crf.split() +
                   watermark.split() + metadata.split() + subtitles.split() + audio_opts.split() + channels.split() + finish.split()))
    proc = await asyncio.create_subprocess_exec(*command, output_filepath, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # Progress Bar
    await handle_progress(proc, msg, message, filepath)
    # Wait for the subprocess to finish
    stdout, stderr = await proc.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    LOGGER.info(e_response)
    LOGGER.info(t_response)
    await proc.communicate()
    return output_filepath


def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
        return None


def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
        return metadata.get('duration').seconds
    else:
        return 0


def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    else:
        return (1280, 720)


async def media_info(saved_file_path):
    process = subprocess.Popen(
        [
            'ffmpeg',
            "-hide_banner",
            '-i',
            saved_file_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout, stderr = process.communicate()
    output = stdout.decode().strip()
    duration = re.search("Duration:\s*(\d*):(\d*):(\d+\.?\d*)[\s\w*$]", output)
    bitrates = re.search("bitrate:\s*(\d+)[\s\w*$]", output)

    if duration is not None:
        hours = int(duration.group(1))
        minutes = int(duration.group(2))
        seconds = math.floor(float(duration.group(3)))
        total_seconds = (hours * 60 * 60) + (minutes * 60) + seconds
    else:
        total_seconds = None
    if bitrates is not None:
        bitrate = bitrates.group(1)
    else:
        bitrate = None
    return total_seconds, bitrate


async def handle_progress(proc, msg, message, filepath):
    name = os.path.basename(filepath)
    # Progress Bar
    COMPRESSION_START_TIME = time.time()
    LOGGER.info("ffmpeg_process: "+str(proc.pid))
    status = download_dir + "status.json"
    with open(status, 'w') as f:
        statusMsg = {
            'running': True,
            'message': msg.id,
            'user': message.from_user.id
        }
        json.dump(statusMsg, f, indent=2)
    with open(status, 'r+') as f:
        statusMsg = json.load(f)
        statusMsg['pid'] = proc.pid
        statusMsg['message'] = msg.id
        statusMsg['user'] = message.from_user.id
        f.seek(0)
        json.dump(statusMsg, f, indent=2)
    while proc.returncode == None:
        await asyncio.sleep(5)
        with open(download_dir + 'process.txt', 'r+') as file:
            text = file.read()
            frame = re.findall("frame=(\d+)", text)
            time_in_us = re.findall("out_time_ms=(\d+)", text)
            progress = re.findall("progress=(\w+)", text)
            speed = re.findall("speed=(\d+\.?\d*)", text)
            if len(frame):
                frame = int(frame[-1])
            else:
                frame = 1
            if len(speed):
                speed = speed[-1]
            else:
                speed = 1
            if len(time_in_us):
                time_in_us = time_in_us[-1]
            else:
                time_in_us = 1
            if len(progress):
                if progress[-1] == "end":
                    LOGGER.info(progress[-1])
                    break
            breakexecution_time = TimeFormatter(
                (time.time() - COMPRESSION_START_TIME))
            elapsed_time = int(time_in_us)/1000000
            total_time, bitrate = await media_info(filepath)
            difference = math.floor((total_time - elapsed_time) / float(speed))
            ETA = "-"
            if difference > 0:
                ETA = TimeFormatter(difference)
            percentage = math.floor(elapsed_time * 100 / total_time)
            progress_str = "<b>Encoding Video:</b> {0}%\n{1}{2}".format(
                round(percentage, 2),
                ''.join(['█' for i in range(
                    math.floor(percentage / 10))]),
                ''.join(['░' for i in range(
                    10 - math.floor(percentage / 10))])
            )
            stats = f'{progress_str} \n' \
                    f'• ETA: {ETA}'
            try:
                await msg.edit(
                    text=stats,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('Cancel', callback_data='cancel'), InlineKeyboardButton(
                                    'Stats', callback_data='stats')
                            ]
                        ]
                    )
                )
            except:
                pass
