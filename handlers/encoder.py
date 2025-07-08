import os
import asyncio
import shlex
import re
import math
import time
import subprocess
from moviepy.editor import VideoFileClip

def get_video_info(path):
    clip = VideoFileClip(path)
    duration = clip.duration  # in seconds
    width, height = clip.size
    resolution = f"{width}x{height}"
    size = os.path.getsize(path) / (1024 * 1024)  # in MB
    return duration, resolution, size

def build_progress_bar(percent, length=20):
    filled = math.floor(length * percent / 100)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {percent:.0f}%"

def get_codec(output_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", output_path],
        capture_output=True, text=True
    )
    return result.stdout.strip().upper()

async def encode_to_x265(input_path, message=None):
    filename = os.path.basename(input_path)
    output_path = f"x265_{filename}"

    total_duration, resolution, original_size = get_video_info(input_path)

    cmd = f"ffmpeg -i {shlex.quote(input_path)} -c:v libx265 -crf 28 -c:a copy {shlex.quote(output_path)} -y"

    start_time = time.time()
    process = await asyncio.create_subprocess_shell(
        cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.DEVNULL
    )

    last_percent = -1
    while True:
        line = await process.stderr.readline()
        if not line:
            break

        decoded = line.decode("utf-8", errors="ignore")
        match = re.search(r"time=(\d+):(\d+):(\d+).(\d+)", decoded)
        if match:
            h, m, s, ms = map(int, match.groups())
            current_sec = h * 3600 + m * 60 + s + ms / 100
            percent = (current_sec / total_duration) * 100
            if percent - last_percent >= 5:
                last_percent = percent
                bar = build_progress_bar(percent)
                try:
                    await message.edit_text(f"🎬 Encoding Progress\n\n{bar}")
                except:
                    pass

    await process.wait()

    if not os.path.exists(output_path):
        raise Exception("❌ Encoding failed. Output not found.")

    end_time = time.time()
    elapsed = end_time - start_time

    final_size = os.path.getsize(output_path) / (1024 * 1024)
    reduction = ((original_size - final_size) / original_size) * 100
    codec = get_codec(output_path)

    mins, secs = divmod(int(elapsed), 60)
    hrs, mins = divmod(mins, 60)
    duration_str = f"{hrs:02}:{mins:02}:{secs:02}"

    stats = (
        "✅ <b>ENCODING COMPLETE!</b>\n\n"
        f"📐 <b>Resolution:</b> {resolution}\n"
        f"🛠️ <b>Codec:</b> {codec}\n"
        f"📦 <b>Original Size:</b> {original_size:.1f}MB\n"
        f"📉 <b>Final Size:</b> {final_size:.1f}MB\n"
        f"📊 <b>Reduction:</b> {reduction:.1f}%\n"
        f"\n⏱️ <b>Processing Time:</b> {duration_str}\n\n"
        "💎 <i>Fast encoding by WD ZONE</i>"
    )

    try:
        await message.edit_text(stats, parse_mode="html")
    except:
        pass

    return output_path
