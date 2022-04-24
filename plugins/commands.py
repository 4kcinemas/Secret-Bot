import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)


BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming & ~filters.edited)
async def start(client, message):
    if message.chat.type in ['group', 'supergroup']:
        buttons = [
            [
                InlineKeyboardButton('➕ Add Me', url=f'http://t.me/netflimbot?startgroup=true'),
                InlineKeyboardButton('ℹ️ Help', url=f'https://t.me/iNetflixRoBot?start=help'),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        parse_mode="markdown"
        disable_web_page_preview=True
        await message.reply(script.START2_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('👥 Support Channel', url='https://t.me/iPRIMEHUB'),
            InlineKeyboardButton("👣 Share Me ", url='https://t.me/share/url?url=&text=%E2%98%BA%EF%B8%8F%20%F0%9D%90%88%27%F0%9D%90%A6%20%F0%9D%90%8C%F0%9D%90%A8%F0%9D%90%AF%F0%9D%90%A2%F0%9D%90%9E%20%F0%9D%90%85%F0%9D%90%A2%F0%9D%90%A7%F0%9D%90%9D%F0%9D%90%9E%F0%9D%90%AB%20%F0%9D%90%81%F0%9D%90%A8%F0%9D%90%AD%0A%F0%9F%91%8C%20%F0%9D%90%88%20%F0%9D%90%82%F0%9D%90%9A%F0%9D%90%A7%20%F0%9D%90%92%F0%9D%90%9E%F0%9D%90%9A%F0%9D%90%AB%F0%9D%90%9C%F0%9D%90%A1%20%F0%9D%90%8C%F0%9D%90%A8%F0%9D%90%AF%F0%9D%90%A2%F0%9D%90%9E%20%F0%9D%90%85%F0%9D%90%A8%F0%9D%90%AB%20%F0%9D%90%98%F0%9D%90%A8%F0%9D%90%AE%0A%F0%9F%98%8B%20%F0%9D%90%89%F0%9D%90%AE%F0%9D%90%AC%F0%9D%90%AD%20%F0%9D%90%92%F0%9D%90%9E%F0%9D%90%A7%F0%9D%90%9D%20%F0%9D%90%8C%F0%9D%90%9E%20%F0%9D%90%80%F0%9D%90%A7%F0%9D%90%B2%20%F0%9D%90%8C%F0%9D%90%A8%F0%9D%90%AF%F0%9D%90%A2%F0%9D%90%9E%20%F0%9D%90%8D%F0%9D%90%9A%F0%9D%90%A6%F0%9D%90%9E%0A%F0%9F%94%AE%20%F0%9D%90%93%F0%9D%90%A1%F0%9D%90%9E%F0%9D%90%A7%20%F0%9D%90%92%F0%9D%90%AD%F0%9D%90%9A%F0%9D%90%A7%F0%9D%90%9D%20%F0%9D%90%81%F0%9D%90%9A%F0%9D%90%9C%F0%9D%90%A4%20%F0%9D%90%80%F0%9D%90%A7%F0%9D%90%9D%20%F0%9D%90%92%F0%9D%90%9E%F0%9D%90%9E%20%F0%9D%90%93%F0%9D%90%A1%F0%9D%90%9E%20%F0%9D%90%8C%F0%9D%90%9A%F0%9D%90%A0%F0%9D%90%A2%F0%9D%90%9C%20%20%0A%F0%9F%98%8E%20%F0%9D%90%81%F0%9D%90%A8%F0%9D%90%AD%F0%9D%90%8B%F0%9D%90%A2%F0%9D%90%A7%F0%9D%90%A4%20-%3E%20%40iNetFlixRoBot')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🥺Join PrimeHub", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            kk, file_id = message.command[1].split("_", 1)
            pre = 'checksubp' if kk == 'filep' else 'checksub' 
            btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{file_id}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="**You Have To Join My Channel To Use This Bot**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode="markdown"
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('📢 Support Channel', url='https://t.me/iPRIMEHUB'),
            InlineKeyboardButton("👣 Share Me ", url='https://t.me/share/url?url=&text=%E2%98%BA%EF%B8%8F%20%F0%9D%90%88%27%F0%9D%90%A6%20%F0%9D%90%8C%F0%9D%90%A8%F0%9D%90%AF%F0%9D%90%A2%F0%9D%90%9E%20%F0%9D%90%85%F0%9D%90%A2%F0%9D%90%A7%F0%9D%90%9D%F0%9D%90%9E%F0%9D%90%AB%20%F0%9D%90%81%F0%9D%90%A8%F0%9D%90%AD%0A%F0%9F%91%8C%20%F0%9D%90%88%20%F0%9D%90%82%F0%9D%90%9A%F0%9D%90%A7%20%F0%9D%90%92%F0%9D%90%9E%F0%9D%90%9A%F0%9D%90%AB%F0%9D%90%9C%F0%9D%90%A1%20%F0%9D%90%8C%F0%9D%90%A8%F0%9D%90%AF%F0%9D%90%A2%F0%9D%90%9E%20%F0%9D%90%85%F0%9D%90%A8%F0%9D%90%AB%20%F0%9D%90%98%F0%9D%90%A8%F0%9D%90%AE%0A%F0%9F%98%8B%20%F0%9D%90%89%F0%9D%90%AE%F0%9D%90%AC%F0%9D%90%AD%20%F0%9D%90%92%F0%9D%90%9E%F0%9D%90%A7%F0%9D%90%9D%20%F0%9D%90%8C%F0%9D%90%9E%20%F0%9D%90%80%F0%9D%90%A7%F0%9D%90%B2%20%F0%9D%90%8C%F0%9D%90%A8%F0%9D%90%AF%F0%9D%90%A2%F0%9D%90%9E%20%F0%9D%90%8D%F0%9D%90%9A%F0%9D%90%A6%F0%9D%90%9E%0A%F0%9F%94%AE%20%F0%9D%90%93%F0%9D%90%A1%F0%9D%90%9E%F0%9D%90%A7%20%F0%9D%90%92%F0%9D%90%AD%F0%9D%90%9A%F0%9D%90%A7%F0%9D%90%9D%20%F0%9D%90%81%F0%9D%90%9A%F0%9D%90%9C%F0%9D%90%A4%20%F0%9D%90%80%F0%9D%90%A7%F0%9D%90%9D%20%F0%9D%90%92%F0%9D%90%9E%F0%9D%90%9E%20%F0%9D%90%93%F0%9D%90%A1%F0%9D%90%9E%20%F0%9D%90%8C%F0%9D%90%9A%F0%9D%90%A0%F0%9D%90%A2%F0%9D%90%9C%20%20%0A%F0%9F%98%8E%20%F0%9D%90%81%F0%9D%90%A8%F0%9D%90%AD%F0%9D%90%8B%F0%9D%90%A2%F0%9D%90%A7%F0%9D%90%A4%20-%3E%20%40iNetFlixRoBot')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("Please wait")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1) 
        await sts.delete()
        return
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("Please wait")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()
        

    """files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        )"""
                   

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


#the end        
