from presets import Presets
from pyrogram.types import Message
from pyrogram import Client, filters
from support.markups import start_buttons


@Client.on_message(filters.private & filters.command('start'))
async def start_bot(c, m: Message):
    await m.reply_text(Presets.WELCOME_TXT.format(m.from_user.first_name), reply_markup=start_buttons)
    await m.delete()
