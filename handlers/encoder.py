# 📁 handlers/encoder.py

import os
import subprocess

async def encode_to_x265(input_path: str) -> str:
    file_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(file_name)[0]
    output_path = f"{name_without_ext}_265.mkv"

    cmd = [
        "ffmpeg", "-i", input_path,
        "-c:v", "libx265", "-preset", "slow", "-crf", "28",
        "-c:a", "copy",  # keep audio
        output_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(output_path):
        raise Exception("Encoding failed ❌")

    return output_path
