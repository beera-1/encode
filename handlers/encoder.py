import os
import asyncio
import shlex
import re
import math
from moviepy.editor import VideoFileClip


def get_duration(input_path):
    clip = VideoFileClip(input_path)
    duration = clip.duration
    clip.close()  # important to release file
    return duration  # in seconds


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

    last_progress_step = -1

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

            progress_step = int(percent // 5)  # update every 5%
            if progress_step != last_progress_step:
                last_progress_step = progress_step
                bar = build_progress_bar(percent)
                text = f"🎬 Encoding Progress: {bar}"
                try:
                    if message and message.text != text:
                        await message.edit_text(text)
                except Exception:
                    pass

    await process.wait()

    if not os.path.exists(output_path):
        raise Exception("❌ Encoding failed. Output not found.")

    return output_path
