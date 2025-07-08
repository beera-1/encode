import os
import asyncio
import shlex
import re
import math
from moviepy.editor import VideoFileClip

def get_duration(input_path):
    clip = VideoFileClip(input_path)
    return clip.duration  # in seconds

def build_progress_bar(percent, length=20):
    filled = math.floor(length * percent / 100)
    bar = '█' * filled + ' ' * (length - filled)
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

    progress_msg = None
    last_percent = -1

    while True:
        line = await process.stderr.readline()
        if not line:
            break

        decoded_line = line.decode("utf-8", errors="ignore")
        match = re.search(r"time=(\d+):(\d+):(\d+).(\d+)", decoded_line)
        if match:
            hours, minutes, seconds, ms = map(int, match.groups())
            current_sec = hours * 3600 + minutes * 60 + seconds + ms / 100
            percent = (current_sec / total_duration) * 100
            if percent - last_percent >= 5 or percent >= 99:
                bar = build_progress_bar(percent)
                try:
                    await message.edit_text(f"🎬 Encoding Progress: {bar}")
                    last_percent = percent
                except:
                    pass

    await process.wait()

    if not os.path.exists(output_path):
        raise Exception("❌ Encoding failed. Output not found.")

    return output_path
