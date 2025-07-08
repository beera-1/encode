import os
import asyncio
import shlex
import re
import math
from moviepy.editor import VideoFileClip
from datetime import datetime

def get_duration(input_path):
    clip = VideoFileClip(input_path)
    return clip.duration  # in seconds

def build_progress_bar(percent, length=20):
    filled = math.floor(length * percent / 100)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {percent:.0f}%"

async def encode_to_x265(input_path, message=None):
    filename = os.path.basename(input_path)
    output_path = f"x265_{filename}"
    total_duration = get_duration(input_path)

    cmd = f"ffmpeg -i {shlex.quote(input_path)} -c:v libx265 -crf 28 -c:a copy {shlex.quote(output_path)} -y"
    process = await asyncio.create_subprocess_shell(
        cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.DEVNULL
    )

    start_time = datetime.now()
    last_progress_step = -1

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

            step = int(percent // 5)
            if step != last_progress_step:
                last_progress_step = step
                bar = build_progress_bar(percent)

                elapsed = (datetime.now() - start_time).seconds
                eta = int(elapsed * ((100 - percent) / max(percent, 1)))
                eta_str = f"{eta // 60}m {eta % 60}s"

                txt = f"🎬 Encoding: {bar}\n⏳ ETA: {eta_str}"

                try:
                    await message.edit_text(txt)
                except:
                    pass  # silently ignore to avoid 'Separator/Chunk' errors

    await process.wait()

    if not os.path.exists(output_path):
        raise Exception("❌ Encoding failed. Output not found.")

    return output_path
