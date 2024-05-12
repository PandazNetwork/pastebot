import os
from pyrogram import Client, filters
from config import API_HASH, API_ID, BOT_TOKEN, ADMIN_IDS
from utilis import paste_api, handle_forcesub
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
async def handle_private_message(bot, message):
    await handle_forcesub(bot, message)
    db.add_user(message.from_user.id)
    
    if message.text:
        paste_link = await paste_api(message.text)
        
        if paste_link:
            await message.reply_text(f"{paste_link}")
        else:
            await message.reply_text("Failed to generate paste link")
    elif message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        
        if document.file_name.endswith(".txt"):
            file_path = await bot.download_media(document)
            
            print("File downloaded:", file_path)
            
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                
            paste_link = await paste_api(text)
            
            if paste_link:
                await message.reply_text(f"Paste link for the file: {paste_link}")
            else:
                await message.reply_text("Failed to generate paste link for the file")
            
            os.remove(file_path)
        else:
            await message.reply_text("Please send only text files (.txt)")


print("[+] BOT STARTED")
if __name__ == "__main__":
    bot.run()
