# 📁 handlers/sample_gen.py

import os
import subprocess

async def generate_sample(input_path: str, duration: int = 30) -> str:
    name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = f"{name}_sample_{duration}s.mkv"

    cmd = [
        "ffmpeg", "-ss", "0", "-i", input_path,
        "-t", str(duration), "-c", "copy", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(output_path):
        raise Exception("Sample generation failed ❌")

    return output_path
