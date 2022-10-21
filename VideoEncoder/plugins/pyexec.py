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

import ast
import asyncio
import html
import inspect
import sys
import traceback
from io import BytesIO

from pyrogram import Client, filters

from .. import memory_file
from ..utils.helper import check_chat


@Client.on_message(filters.command('exec'))
async def run_code(client, message):
    c = await check_chat(message, chat='Sudo')
    if c is None:
        return

    class UniqueExecReturnIdentifier:
        pass
    code = message.text[5:].strip()
    if not code:
        await message.reply_text('code 100')
        return
    tree = ast.parse(code)
    obody = tree.body
    body = obody.copy()
    body.append(ast.Return(ast.Name('_ueri', ast.Load())))

    def _gf(body):
        # args: m, message, c, client, _ueri
        func = ast.AsyncFunctionDef('ex', ast.arguments([], [ast.arg(i, None, None) for i in [
                                    'm', 'message', 'c', 'client', '_ueri']], None, [], [], None, []), body, [], None, None)
        ast.fix_missing_locations(func)
        mod = ast.parse('')
        mod.body = [func]
        fl = locals().copy()
        exec(compile(mod, '<ast>', 'exec'), globals(), fl)
        return fl['ex']
    try:
        exx = _gf(body)
    except SyntaxError as ex:
        if ex.msg != "'return' with value in async generator":
            raise
        exx = _gf(obody)
    escaped_code = html.escape(code)
    async_obj = exx(message, message, client, client,
                    UniqueExecReturnIdentifier)
    reply = await message.reply_text('Type[py]\n<code>{}</code>\nState[Executing]'.format(escaped_code))
    stdout = sys.stdout
    stderr = sys.stderr
    wrapped_stdout = memory_file(bytes=False)
    wrapped_stdout.buffer = memory_file()
    wrapped_stderr = memory_file(bytes=False)
    wrapped_stderr.buffer = memory_file()
    sys.stdout = wrapped_stdout
    sys.stderr = wrapped_stderr
    try:
        if inspect.isasyncgen(async_obj):
            returned = [i async for i in async_obj]
        else:
            returned = [await async_obj]
            if returned == [UniqueExecReturnIdentifier]:
                returned = []
    except Exception:
        await message.reply_text(traceback.format_exc(), parse_mode=None)
        return
    finally:
        sys.stdout = stdout
        sys.stderr = stderr
    wrapped_stdout.seek(0)
    wrapped_stderr.seek(0)
    wrapped_stdout.buffer.seek(0)
    wrapped_stderr.buffer.seek(0)
    r = []
    outtxt = wrapped_stderr.read() + wrapped_stderr.buffer.read().decode()
    if outtxt.strip().strip('\n').strip():
        r.append(outtxt)
    errtxt = wrapped_stdout.read() + wrapped_stdout.buffer.read().decode()
    if errtxt.strip().strip('\n').strip():
        r.append(errtxt)
    r.extend(returned)
    r = [html.escape(str(i).strip('\n')) for i in r]
    r = '\n'.join([f'<code>{i}</code>' for i in r])
    r = r.strip() or 'undefined'
    await reply.edit_text('Type[py]\n<code>{}</code>\nState[Executed]\nOutput \\\n{}'.format(escaped_code, r))


@Client.on_message(filters.command('sh'))
async def run_shell(client, message):
    c = await check_chat(message, chat='Sudo')
    if c is None:
        return
    command = message.text.split(None, 1)[1]
    if not command:
        await message.reply_text('code 100')
        return
    reply = await message.reply_text('Executing...')
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    returncode = process.returncode
    text = f'<b>Exit Code:</b> <code>{returncode}</code>\n'
    stdout = stdout.decode().replace('\r', '').strip('\n').rstrip()
    stderr = stderr.decode().replace('\r', '').strip('\n').rstrip()
    if stderr:
        text += f'<code>{html.escape(stderr)}</code>\n'
    if stdout:
        text += f'<code>{html.escape(stdout)}</code>'

    # send as a file if it's longer than 4096 bytes
    if len(text) > 4096:
        out = stderr.strip() + "\n" + stdout.strip()
        f = BytesIO(out.strip().encode('utf-8'))
        f.name = "output.txt"
        await reply.delete()
        await message.reply_document(f, caption=f'<b>Exit Code:</b> <code>{returncode}</code>')
    else:
        await reply.edit_text(text)
