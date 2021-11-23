from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .. import sudo_users

start = InlineKeyboardMarkup([
    [InlineKeyboardButton("Support", url="https://t.me/joinchat/4PQUG5J6aRI3NGQ1"),
     InlineKeyboardButton("Channel", url="https://t.me/WeebZoneIndia")],
    [InlineKeyboardButton("Developer", url="https://github.com/WeebTime/"),
     InlineKeyboardButton("Source", url="https://github.com/WeebTime/Video-Encoder-Bot")]
])

output = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer", url="https://github.com/WeebTime/"),
     InlineKeyboardButton("Source", url="https://github.com/WeebTime/Video-Encoder-Bot")]
])

async def check_user(message):
    user_id = message.from_user.id
    if user_id in sudo_users:
        return 'Sudo'
    else:
        text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>,\nI can encode telegram files in x264 but unfourtunately you have to deploy one for yourself."
        await message.reply(text=text, reply_markup=start)
        return None