# 📁 handlers/screenshots.py

import os
import subprocess

async def generate_screenshots(input_path: str, count: int = 5) -> list:
    screenshots = []
    for i in range(1, count + 1):
        output_file = f"screenshot_{i}.jpg"
        timestamp = i * 10
        cmd = [
            "ffmpeg", "-ss", str(timestamp), "-i", input_path,
            "-frames:v", "1", "-q:v", "2", output_file
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(output_file):
            screenshots.append(output_file)
    return screenshots
