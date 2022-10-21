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
from urllib.parse import unquote_plus

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .. import data
from ..utils.database.add_user import AddUserToDatabase
from ..utils.helper import check_chat

queue_callback_filter = filters.create(
    lambda _, __, query: query.data.startswith('queue+'))


async def get_title(i):
    try:
        if data[i].video:
            return data[i].video.file_name
        elif data[i].document:
            return data[i].document.file_name
        else:
            url = data[i].command[1]
            return str(unquote_plus(os.path.basename(url)))
    except:
        return None


def map(pos):
    if pos == 0:
        if len(data) > 1:
            button = [[InlineKeyboardButton(
                text='Next', callback_data="queue+1")]]
        else:
            button = [[InlineKeyboardButton(
                text='No Other Task', callback_data="queue+-1")]]
    else:
        try:
            if data[pos+1]:
                button = [
                    [
                        InlineKeyboardButton(
                            text='Previous', callback_data=f"queue+{pos-1}"),
                        InlineKeyboardButton(
                            text='Next', callback_data=f"queue+{pos+1}")
                    ],
                ]
        except Exception as e:
            button = [
                [
                    InlineKeyboardButton(
                        text='Previous', callback_data=f"queue+{pos-1}")
                ],
            ]
    return button


async def queue_answer(app, callback_query):
    chatid = callback_query.from_user.id
    messageid = callback_query.message.id
    pos = int(callback_query.data.split('+')[1])
    if pos == -1:
        await callback_query.answer("no task", show_alert=True)
        return
    taskpos = pos+1
    size = len(data)
    tasktitle = await get_title(pos)
    await callback_query.edit_message_text(f"<b>{taskpos} of {size}</b>:\n\n{tasktitle}", reply_markup=InlineKeyboardMarkup(map(pos)))


@Client.on_message(filters.command(['queue']))
async def queue_message(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    msg = await message.reply_text("Wait Checking...")
    size = len(data)
    if size >= 1:
        for i in range(1, size):
            pos = i-1
            taskpos = i
            tasktitle = await get_title(pos)
            await msg.edit(
                text=f"<b>{taskpos} of {size}</b>:\n\n{tasktitle}", reply_markup=InlineKeyboardMarkup(map(0)))
    else:
        await msg.edit('🥱 No Active Encodes.')


@Client.on_message(filters.command('clear'))
async def clear(app, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    await AddUserToDatabase(app, message)
    if len(data) >= 1:
        current = data[0]
        data.clear()
        data.append(current)
        await message.reply('Purged all tasks!')
    else:
        await message.reply("🥱 No Active Encodes.")
