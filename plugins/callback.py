#disable for now
#Causing pm_filter error....
"""
import os
from asyncio import Future, sleep
import time
from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

#buttons
HELP_BUTTON = [[
InlineKeyboardButton('⚠️ Disclaimer', callback_data="disclaimer"), 
InlineKeyboardButton('ℹ️ FeedBack', url=f'https://t.me/PrimeFeedbackBot'),
]]

DISCLAIMER_BUTTON = [[
            InlineKeyboardButton('ℹ️ Report Us', url=f'https://t.me/PrimeFeedbackBot'),
            InlineKeyboardButton('🚫 Close', callback_data="back_data")
        ]]
        
#filter
#help message
@Client.on_message(filters.command("help") & filters.incoming & ~filters.edited)
def help(client, message):
    text = script.HELP_TXT
    reply_markup = InlineKeyboardMarkup(HELP_BUTTON)
    t = message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    time.sleep(150)
    t.delete()
    message.delete(message.message_id)

#callback features        
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "back_data":
        await query.message.delete()
    elif query.data == "disclaimer":
        buttons = [[
            InlineKeyboardButton('ℹ️ Report Us', url=f'https://t.me/PrimeFeedbackBot'),
            InlineKeyboardButton('🚫 Close', callback_data="back_data")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DISCLAIMER_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
"""
