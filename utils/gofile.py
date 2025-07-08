# 📁 utils/gofile.py

import requests

def upload_to_gofile(file_path: str) -> str:
    try:
        url = "https://upload.gofile.io/uploadFile"
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files, timeout=300)

        data = response.json()

        if data.get("status") == "ok":
            return data["data"]["downloadPage"]
        else:
            raise Exception("Gofile upload failed")

    except Exception as e:
        print(f"[Gofile Error] {e}")
        return None
