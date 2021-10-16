from pyrogram import Client, filters
from pyrogram.types import CallbackQuery


@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close_button(c, cb: CallbackQuery):
    await cb.message.delete()
