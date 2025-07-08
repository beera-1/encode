import asyncio
import os
import re

async def encode_to_x265(input_path, message=None):
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_path = f"{name}_x265{ext}"

    cmd = [
        "ffmpeg", "-i", input_path,
        "-c:v", "libx265", "-preset", "medium",
        "-crf", "28",
        "-c:a", "copy",
        output_path,
        "-y"
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    duration = None
    pattern_time = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

    async for line in process.stderr:
        decoded = line.decode("utf-8", errors="ignore")

        # extract video duration
        if not duration and "Duration" in decoded:
            dur_match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", decoded)
            if dur_match:
                h, m, s = map(float, dur_match.groups())
                duration = h * 3600 + m * 60 + s

        # extract current time during encoding
        if duration:
            time_match = pattern_time.search(decoded)
            if time_match:
                h, m, s = map(float, time_match.groups())
                current = h * 3600 + m * 60 + s
                percent = int((current / duration) * 100)
                bar = build_progress_bar(percent)
                if message:
                    try:
                        await message.edit_text(f"⏳ Encoding: {bar} {percent}%")
                    except:
                        pass  # Ignore if Telegram flood limits

    await process.wait()
    return output_path

def build_progress_bar(percent, length=20):
    filled = int(length * percent / 100)
    return "[" + "█" * filled + "░" * (length - filled) + "]"
