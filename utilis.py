import aiohttp, asyncio
from config import FORCESUB, SUPPORT
from pyrogram import enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def paste_api(text):
    url = "https://api.pastes.dev/post"
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=text.encode('utf-8'), headers=headers) as response:
                if response.status == 201:
                    data = await response.json()
                    paste_key = data["key"]
                    return f"https://pastes.dev/{paste_key}"
                else:
                    return None
        except aiohttp.ClientError as e:
            return None
    
async def handle_forcesub(bot, message):
    try:
        invite_link = await bot.create_chat_invite_link(int(FORCESUB))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    try:
        user = await bot.get_chat_member(int(FORCESUB), message.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Sorry Sir, You are Banned. Contact me at {SUPPORT}",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=message.id,
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Mᴇ!\n\nDᴜᴇ ᴛᴏ Oᴠᴇʀʟᴏᴀᴅ, Oɴʟʏ Cʜᴀɴɴᴇʟ Sᴜʙsᴄʀɪʙᴇʀs Cᴀɴ Usᴇ Mᴇ!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 🤖", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_to_message_id=message.id,
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Something Went Wrong. Contact me at {SUPPORT}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_to_message_id=message.id,
        )
        return 400