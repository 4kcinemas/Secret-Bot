#Kanged From @TroJanZheX
import asyncio
import time
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, BUTTON, IGNR
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from Script import script
import re
from pyrogram.errors import UserNotParticipant
from utils2 import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}
IGNR=IGNR.replace(", ", "|")

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Due To Overload Only Channel Subscriber Can Use This Bot :-**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📢 Join SS_Linkz", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 1 < len(message.text) < 100:    
        btn = []
        search = message.text
        if search:
           search = search.replace("#request", "").replace("#Request", "").replace("#REQUEST", "").replace("Please send me", "").replace("please send me", "").replace("Please Send", "").replace("Please send", "").replace("please send", "").replace("plz send", "").replace("Plz Send", "").replace("PLZ SEND", "").replace("give me", "").replace("Give me", "").replace("Give Me", "").replace("GIVE ME", "").replace("# request", "").replace("# Request", "")
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                if filename:
                   filename = filename.replace("[Telegram@Primeroom]", "").replace("[TG@Primeroom]", "").replace("TG@Primeroom", "").replace("Telegram@Primeroom_", "").replace("mkv", "").replace("#", "").replace("Filmy4wap", "").replace("[movies_unload]", " ").replace(".mkv", " ").replace("[Telegram@TheDealsRoom]", " ").replace(".com", " ").replace(".xyz", " ").replace("www", " ").replace("otthd", " ").replace("[Telegram@PrimeroomBkp]","").replace("_", " ").replace("www_", " ").replace("@ottHD", "").replace("@Movies_Unloaded", "").replace("[TG@Primeroom]", "").replace("[Primeroom]", "").replace("[Telegram@Primeroombkp]", " ").replace("[telegram@primeroom]", "").replace("Toonworld4all ", "")  #re.sub(IGNR, r"", )
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )

        else:
            sk = await message.reply_text(
                      text = "**No Results Found \nPlease Check Your Spelling Whether It's Correct or Not🥲**""",
                      reply_markup=InlineKeyboardMarkup(
                      [
                        [InlineKeyboardButton('🔍 Check Your Spelling', url=f'https://www.google.com/search?q={message.text.replace(" ", "%20").replace("#request", "")}%20movie')],
                        [InlineKeyboardButton('🗓️ Check Release Date', url=f'https://www.google.com/search?q={message.text.replace(" ", "%20").replace("#request", "")}%20movie%20release%20date')]
                      ] 
                      ),
                      reply_to_message_id=message.message_id,
                      parse_mode="markdown"
            )
            await asyncio.sleep(30)
            await sk.delete()
            await message.delete(message.message_id)
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                rm = await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(60)
                await rm.delete()
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            fd = await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(60)
            await fd.delete()

"""@Client.on_message(filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=rahul_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
"""

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption:
                   f_caption = f_caption.replace("[Telegram@Primeroom]", "").replace("[Telegram@Primeroom] ", "").replace("TG@Primeroom", "").replace("Telegram@Primeroom_", "").replace("[movies_unload]", "").replace(".mkv", "").replace("Filmy4wap", "").replace("[Telegram@TheDealsRoom]", "").replace(".com", "").replace(".xyz", "").replace("www", "").replace("otthd", "").replace("_", " ").replace("www_", "").replace("[TG@Primeroom]", "").replace("[TelegramPrimeroomBkp]", "").replace("[@ottHD]", "").replace("[telegram@primeroom]", "").replace(".", " ").replace("[Telegram@PrimeroomBkp]", "").replace("[Toonworld4all] ", "")     #re.sub(IGNR, r"", 
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('📢 Support Channel', url='https://t.me/ss_linkz'),
                        InlineKeyboardButton('🗣️ Request Movies', url='https://t.me/NetFlix_Movies_Group')
                    ]
                    ]
                await query.answer()
                tk = await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"```{f_caption}``` \n```Uploaded By``` -> **<a href=https://t.me/netflixautofilterbot>𝗡𝗘𝗧𝗙𝗟𝗜𝗫</a>**",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                time.sleep(1)
                rr = await client.send_message(
                chat_id=query.from_user.id,
                text="**🐾 Files Will Be Deleted Within 10 Mins..**\n__Please Make Sure That You Forward These Files To Your Saved Message or Friends.__",
                reply_to_message_id=query.message.message_id,
                )
                await asyncio.sleep(45)
                await query.message.delete()
                await asyncio.sleep(554)
                await tk.delete()
                await rr.delete()
                ft = await client.send_message(
                chat_id=query.from_user.id,
                text="__⊘ This message was deleted__"
                )
                await asyncio.sleep(1800)
                await ft.delete()

        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(f"I Like Your Smartness, But Don't Be Oversmart 😒")
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption:
                    f_caption = f_caption
                if f_caption is None:
                    f_caption = f"{title} \n━━━━━━━━━━✧❂✧━━━━━━━━━━\n<a href=https://t.me/Netflix_Filter_Bot>🅽🅴🆃🅵🅻🅸🆇</a>",
                buttons = [
                    [
                        InlineKeyboardButton('📢Support Channel', url='https://t.me/ss_linkz'),
                        InlineKeyboardButton('🗣️ Request Movies', url='https://t.me/NetFlix_Movies_Group')
                    ]
                    ]

                await query.answer()
                tm = await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                await asyncio.sleep(300)
                await tm.delete()

        elif query.data == "pages":
            await query.answer()
        elif query.data == "close":
            try:
                await query.message.reply_to_message.delete()
                await query.message.delete()
            except:
                await query.message.delete()
                
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)
