from gc import callbacks

from aiogram.types import keyboard_button, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/help')],
        [KeyboardButton(text='/start')],
        [KeyboardButton(text='/info')],
        [KeyboardButton(text='/survey')]
    ],
    resize_keyboard=True
)


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='GOOGLE', url='https://google.com')],
        [InlineKeyboardButton(text='YOUTUBE', url='https://www.youtube.com')],
    ]
)