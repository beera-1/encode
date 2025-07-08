📁 README.md

# 🎥 Telegram Video Encoder Bot (x264 ➜ x265)

A powerful Telegram bot that:
- 🔁 Converts videos from **x264 to x265 (HEVC)**
- 📸 Generates **screenshots** (5 or 10)
- 🎞️ Creates **sample video clips** (30s, 60s, 120s, 150s)
- 📤 Uploads files to **Telegram or Gofile** (handles 4GB+ files)
- ☁️ Deployable to **Koyeb** with Flask + Docker + Gunicorn

---

## 🚀 Features

✅ Convert video from x264 to x265 (with audio)  
✅ Screenshot generation (1–5 or 1–10 frames)  
✅ Sample clip generation with user-defined duration  
✅ Inline buttons for easy control  
✅ Upload to Telegram or Gofile  
✅ Docker-ready for easy deployment  
✅ Persistent webhook using Flask  
✅ Supports `.mp4`, `.mkv`, `.avi`, `.mov` formats

---

## 📂 Folder Structure

video-encoder-bot/ ├── main.py ├── config.py ├── Dockerfile ├── requirements.txt ├── Procfile ├── runtime.txt ├── .dockerignore ├── handlers/ │   ├── encoder.py │   ├── screenshots.py │   └── sample_gen.py └── utils/ └── gofile.py

---

## 🔧 Environment Variables

Set these in your `.env` file or on **Koyeb → App Settings → Variables**:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
WEBHOOK_URL=https://your-koyeb-app.koyeb.app


---

📦 Requirements

Install required Python packages:

pip install -r requirements.txt

> ffmpeg is required and installed via Dockerfile on Koyeb




---

🐳 Docker Setup (Local or Custom Deployment)

1. Build Docker Image

docker build -t tg-video-bot .

2. Run the Bot

docker run -d -p 8080:8080 --env-file .env tg-video-bot

> Webhook must point to your public server or use ngrok for local testing




---

☁️ Koyeb Deployment (Recommended)

1. Push your project to GitHub


2. Go to https://www.koyeb.com → New App


3. Select your GitHub repo


4. Choose Dockerfile mode


5. Add environment variables:

API_ID, API_HASH, BOT_TOKEN, WEBHOOK_URL



6. Deploy — done! 🎉




---

💬 Bot Usage Flow

1. Send video or movie file to bot (mp4, mkv, etc.)


2. Choose:

🎥 Convert to x265

📸 Generate screenshots (5/10)

🎞️ Generate sample (30/60/120/150s)



3. Choose upload method:

📤 Telegram

🌐 Gofile (for >2GB)





---

👨‍💻 Developer

Made by Survivor
Telegram: @Survivor


---

⚠️ Disclaimer

This tool is for educational and personal use only. Do not use for piracy or violating copyright laws.


---

Happy Encoding 💻🎬🔥

---

📌 You can now copy this as your official `README.md`.  
Let me know if you want badges, license info, or GitHub Actions setup too bro 💪😂

