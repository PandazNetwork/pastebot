import os, time
from pyrogram import Client, filters
from config import API_HASH, API_ID, BOT_TOKEN, ADMIN_IDS
from utilis import paste_api, handle_forcesub
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from database import db

# Pyrogram bot setup
bot = Client("Pastes.Dev Bot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN
             )

# Handler for /start command
@bot.on_message(filters.private & filters.command("start"))
async def start_command(bot, message):
    db.add_user(message.from_user.id)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Updates Channel", url="https://t.me/telebotsupdate"),
                InlineKeyboardButton("📞 Support", url="https://t.me/drwhitexbot")
            ]
        ]
    )
    await message.reply_text(
        f"**Hello! {message.from_user.first_name} ❤️❤️\n\nWelcome to Paste Bot! Send me any text or txt file. I will provide you link.**",
        reply_markup=keyboard
    )

# Define the command handler for /send
@bot.on_message(filters.command("send") & filters.user(ADMIN_IDS))
def send_message(client, message):
    if message.reply_to_message:
        replied_message = message.reply_to_message

        success_count = 0
        error_count = 0

        user_ids = db.get_all_user_ids()

        for user_id in user_ids:
            try:
                if replied_message.text:
                    client.send_message(user_id, replied_message.text)
                elif replied_message.photo:
                    client.send_photo(user_id, photo=replied_message.photo.file_id, caption=replied_message.caption)
                else:
                    pass

                success_count += 1
            except Exception as e:
                print(f"Failed to send message to user {user_id}: {str(e)}")
                if "USER_IS_BLOCKED" in str(e):
                    print(f"User {user_id} is blocked. Removing from database...")
                    db.remove_user(user_id)
                else:
                    error_count += 1
        success_text = f"**Message successfully sent to {success_count} users.**" if success_count > 0 else "**No users were sent the message.**"
        error_text = f"**Failed to send message to {error_count} users.**" if error_count > 0 else "**All messages sent successfully.**"

        message.reply_text(success_text + "\n" + error_text)

# Define the command handler for /stats
@bot.on_message(filters.command("stats") & filters.user(ADMIN_IDS))
async def stats_command(client, message):
    total_users = db.get_total_users_count()
    await message.reply(f"**📊 Statistics\n\nTotal Users On Bot: {total_users}**")

# Define the command handler for text to link convert
@bot.on_message(filters.private)
async def my_event_handler(client: Client, message: Message):
    try:
        await handle_forcesub(client, message)
        db.add_user(message.from_user.id)

        if message.document:
            file_path = await message.download(f"temp/{time.time()}.txt")
            with open(file_path, 'r') as file:
                text = file.read()
            os.remove(file_path)
        else:
            text = message.text
        
        url = await paste_api(text)
        if url:
            await client.send_message(
                chat_id=message.chat.id,
                text=url,
                reply_to_message_id=message.id,  # Correct attribute
                disable_web_page_preview=True
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text="Something went wrong.",
                reply_to_message_id=message.id  # Correct attribute
            )
    except Exception as e:
        await client.send_message(
            chat_id=message.chat.id,
            text=f"Something went wrong: {str(e)}",
            reply_to_message_id=message.id  # Correct attribute
        )
        
print("[+] BOT STARTED")
if __name__ == "__main__":
    bot.run()
