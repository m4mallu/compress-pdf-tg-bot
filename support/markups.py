from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = [
    [
        InlineKeyboardButton("Support", url="t.me/rmprojects"),
        InlineKeyboardButton("Source", url="github.com/m4mallu"),
    ]
]

close = [
    [
        InlineKeyboardButton("Support", url="t.me/rmprojects"),
        InlineKeyboardButton("Close", callback_data="close_btn"),
    ]
]

start_buttons = InlineKeyboardMarkup(start)
close_button = InlineKeyboardMarkup(close)
