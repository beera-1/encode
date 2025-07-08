import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.encoder import encode_to_x265
from handlers.screenshots import generate_screenshots
from handlers.sample_gen import generate_sample
from utils.gofile import upload_to_gofile

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_video_paths = {}

@bot.on_message(filters.private & (filters.video | filters.document))
async def handle_video(client, message):
    video = message.video or message.document
    if not video.file_name.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
        return await message.reply("❗ Unsupported format. Only .mp4, .mkv, .avi, .mov allowed.")

    status = await message.reply("📥 Downloading file...")
    input_path = await message.download()
    user_video_paths[message.from_user.id] = input_path

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Convert to x265", callback_data="convert")],
        [InlineKeyboardButton("📸 Screenshot (1-5)", callback_data="screenshot5"),
         InlineKeyboardButton("📸 Screenshot (1-10)", callback_data="screenshot10")],
        [InlineKeyboardButton("🎞️ Sample 30s", callback_data="sample30"),
         InlineKeyboardButton("🎞️ Sample 60s", callback_data="sample60")],
        [InlineKeyboardButton("🎞️ Sample 120s", callback_data="sample120"),
         InlineKeyboardButton("🎞️ Sample 150s", callback_data="sample150")]
    ])
    await status.edit("✅ Downloaded! Choose action:", reply_markup=buttons)

@bot.on_callback_query()
async def callback_handler(client, callback):
    user_id = callback.from_user.id
    input_path = user_video_paths.get(user_id)
    if not input_path:
        return await callback.answer("❗ No video found.", show_alert=True)

    data = callback.data
    if data == "convert":
        await callback.message.edit("🎬 Encoding to x265...")
        try:
            output_path = await encode_to_x265(input_path)
        except Exception as e:
            return await callback.message.edit(f"❌ Encoding failed: {e}")

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Upload to Telegram", callback_data=f"tg|{output_path}")],
            [InlineKeyboardButton("🌐 Upload to Gofile", callback_data=f"gofile|{output_path}")]
        ])
        await callback.message.edit("✅ Done! Choose upload method:", reply_markup=buttons)

    elif data.startswith("tg|"):
        path = data.split("|", 1)[1]
        filename = os.path.basename(path)
        caption = f"✅ Encoded by Survivor\n🎞️ `{filename}`"
        await callback.message.reply_video(video=path, caption=caption)

    elif data.startswith("gofile|"):
        path = data.split("|", 1)[1]
        await callback.message.edit("🌐 Uploading to Gofile...")
        link = upload_to_gofile(path)
        if link:
            await callback.message.edit(f"✅ Uploaded:\n🔗 {link}")
        else:
            await callback.message.edit("❌ Gofile upload failed.")

    elif data.startswith("screenshot"):
        count = int(data.replace("screenshot", ""))
        await callback.message.edit(f"📸 Creating {count} screenshots...")
        try:
            shots = await generate_screenshots(input_path, count)
            for shot in shots:
                await callback.message.reply_photo(photo=shot)
                os.remove(shot)
        except Exception as e:
            await callback.message.edit(f"❌ Screenshot error.\n{e}")

    elif data.startswith("sample"):
        duration = int(data.replace("sample", ""))
        await callback.message.edit(f"🎞️ Creating sample ({duration}s)...")
        try:
            sample = await generate_sample(input_path, duration)
            await callback.message.reply_video(video=sample, caption=f"🎞️ {duration}s sample")
            os.remove(sample)
        except Exception as e:
            await callback.message.edit(f"❌ Sample error.\n{e}")

    await callback.answer()

if __name__ == "__main__":
    print("✅ Bot started (Polling mode)")
    bot.run()

# 🟢 Keep Koyeb TCP port 8080 alive
import socket
import threading

def keep_port_8080_open():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(1)
    while True:
        conn, _ = sock.accept()
        conn.close()

threading.Thread(target=keep_port_8080_open, daemon=True).start()
