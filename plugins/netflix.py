import os
import random
from asyncio import Future, sleep
import time
from Script import script
from info import BLIST, STKR
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

#txt messages
MOREBOTS_TXT = """**Here Some Of Our Cool Prime Bots That You Can Use Freely Without Any Limitation😊**"""
INLINE_TXT = """**Search........**
"""
PIK = 'https://telegra.ph/file/f4d232fde3824518ae623.jpg'
PIK2 = 'https://telegra.ph/file/67474faec309ca88f7a71.jpg'
DONATE_QR = 'https://telegra.ph/file/97424ec12aabfe9b4b58c.jpg'

#buttons
DONATE_BUTTON = [[
InlineKeyboardButton('🙋 Developer', url=f'https://t.me/h7n9_alpha'), 
InlineKeyboardButton('👥 Support Channel', url=f'https://t.me/iprimehub'),
]]

REQUEST_BUTTON = [[
InlineKeyboardButton('📢 Support Channel', url=f'https://t.me/iPrimeHub'), 
InlineKeyboardButton('👥 Request Content', url=f'https://t.me/NetFlixRequestChat'),
]]

HELP_BUTTON = [[
InlineKeyboardButton('⚠️ Disclaimer', url=f'https://telegra.ph/DISCLAIMER-03-12-15'), 
InlineKeyboardButton('ℹ️ FeedBack', url=f'https://t.me/PrimeFeedbackBot'),
]]

DISCLAIMER_BUTTON = [[
            InlineKeyboardButton('🫂 Credit', url=f'https://telegra.ph/CREDIT-04-09'),
            InlineKeyboardButton('ℹ️ Report', url=f'https://t.me/PrimeFeedbackBot')
        ]]

MOREBOTS_BUTTON = [
            [
            InlineKeyboardButton('🔗 File To Link Bot', url=f'https://t.me/FileLinkRBot'),
            InlineKeyboardButton('🥷 Force Subscribe Bot', url=f'https://t.me/primesubs_bot'),
            ],[
            InlineKeyboardButton('🐾 Request Tracker Bot', url=f'https://t.me/primecaption_bot'),
            InlineKeyboardButton('🖊️ Files Renamer Bot', url=f'https://t.me/PrimeRenamersBot'),
            ],[
            InlineKeyboardButton('🖇️ Link Shortner Bot', url=f'https://t.me/primeshort_bot'),
            InlineKeyboardButton('📥 URL Uploader Bot', url=f'https://t.me/PrimeDownloderBot'),
            ],[
            InlineKeyboardButton('🍆 Torrent Search Bot', url=f'https://t.me/PRIMETOROBot'),
            InlineKeyboardButton('🔥 Torrent Leeching ', url=f'https://t.me/PrimeLeech'),
            ]
         ]

INLIN_BTN = [[
            InlineKeyboardButton('🏡 Search Somewhere', switch_inline_query=""),
            InlineKeyboardButton('🔍 Search Here', switch_inline_query_current_chat=""),
            ]]

#donate message
@Client.on_message(filters.command('donate') & filters.incoming & ~filters.edited)      #DONATE COMMANDS AND MASSAGES
def donate(bot, message): 
    reply_markup = InlineKeyboardMarkup(DONATE_BUTTON)
    q = message.reply_photo(
        photo=DONATE_QR,
        caption=script.DONATE_MESSAGE,
        parse_mode='html',
    )
    time.sleep(300)
    q.delete()
    message.delete(message.message_id)
 
#request message
@Client.on_message(filters.command("request") & filters.incoming & ~filters.edited)
def request(client, message):
    reply_markup = InlineKeyboardMarkup(REQUEST_BUTTON)
    w = message.reply_photo(
        photo=PIK2,
        caption = script.REQUEST_TXT,
        reply_markup=reply_markup,
        parse_mode='html',
    )
    time.sleep(30)
    w.delete()
    message.delete(message.message_id)

#help message
@Client.on_message(filters.command("help") & filters.incoming & ~filters.edited)
def help(client, message):
    text = script.HELP_TXT
    reply_markup = InlineKeyboardMarkup(HELP_BUTTON)
    t = message.reply(
        text=text,
        reply_to_message_id=message.message_id,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    time.sleep(120)
    t.delete()
    message.delete(message.message_id)

#disclaimer message
@Client.on_message(filters.command('disclaimer') & filters.incoming & ~filters.edited)      
def disclaimer(bot, message):
    text = script.DISCLAIMER_TXT
    reply_markup = InlineKeyboardMarkup(DISCLAIMER_BUTTON)
    l = message.reply(
        text=text,
        reply_to_message_id=message.message_id,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    time.sleep(60)
    l.delete()
    message.delete(message.message_id)

#more bots message
@Client.on_message(filters.command('morebots') & filters.private & filters.incoming & ~filters.edited)     
def morebots(bot, message):
    text = MOREBOTS_TXT
    reply_markup = InlineKeyboardMarkup(MOREBOTS_BUTTON)
    n = message.reply(
        text=text,
        reply_to_message_id=message.message_id,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    time.sleep(20)
    n.delete()
    message.delete(message.message_id)

#inline message
@Client.on_message(filters.command("inlinex") & filters.incoming & ~filters.edited)
def searches(client, message):
    reply_markup = InlineKeyboardMarkup(INLIN_BTN)
    xt = message.reply_photo(
        photo=PIK,
        reply_markup=reply_markup,
        parse_mode='html',
    )
    time.sleep(120)
    xt.delete()
    message.delete(message.message_id)

#annoy
BLIST = BLIST.replace(", ","|")
@Client.on_message(filters.regex(r"(chutiya|Chutiya|chomu|Chomu|limde|Limde|chodarmad|Chodarmad|nudes|Nudes|porn|Porn|hentai|Hentai|motherchod|Motherchod|bhenchod|Bhenchod|benchod|salle|Salle|sex videos|Sex Videos|Sex videos|bf|Bf|BF|porn videos|Porn Videos|Porn videos|boobs|Boobs|BOOBS|bhosdike|Bhosdike|bsdk|BSDK|bitch|Bitch|BITCH|savita bhabhi|Savita Bhabhi|gandu|Gandu|harami|Harami|Haarami)") | filters.regex(BLIST) & filters.private & filters.incoming & ~filters.edited)      
def regex(bot, message):
    gj = message.reply_sticker(sticker=random.choice(STKR)
    )
    time.sleep(10)
    gj.delete()
    message.delete(message.message_id
    )
    return

