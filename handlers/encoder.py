import asyncio
import os
import re

async def encode_to_x265(input_path, message=None):
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_path = f"{name}_x265{ext}"

    # Step 1: Get duration using ffprobe
    duration = await get_duration(input_path)
    if not duration:
        raise Exception("❌ Unable to fetch duration.")

    # Step 2: Build ffmpeg command
    cmd = [
        "ffmpeg", "-i", input_path,
        "-c:v", "libx265", "-preset", "medium",
        "-crf", "28", "-c:a", "copy",
        "-y", output_path
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )

    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")
    last_percent = -1

    # Step 3: Read ffmpeg stderr line by line
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        decoded = line.decode("utf-8", errors="ignore")
        match = time_pattern.search(decoded)
        if match:
            h, m, s = map(float, match.groups())
            current = h * 3600 + m * 60 + s
            percent = int((current / duration) * 100)
            if percent != last_percent:
                last_percent = percent
                bar = build_progress_bar(percent)
                if message:
                    try:
                        await message.edit(f"🎬 Encoding:\n{bar} {percent}%")
                    except:
                        pass  # Ignore Telegram rate limits

    await process.wait()
    return output_path

# Step 4: ffprobe to get total video duration
async def get_duration(input_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_path
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    stdout, _ = await process.communicate()
    try:
        return float(stdout.decode().strip())
    except:
        return None

# Step 5: Build progress bar with filled blocks
def build_progress_bar(percent, length=20):
    filled = int(length * percent / 100)
    return "[" + "█" * filled + "░" * (length - filled) + "]"
