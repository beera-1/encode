# 🐍 Base Python image
FROM python:3.11-slim

# 📁 Set work directory
WORKDIR /app

# 🛠️ Install ffmpeg & dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && apt-get clean

# 📦 Copy bot code
COPY . .

# 📦 Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Expose port for Koyeb TCP health check
EXPOSE 8080

# 🚀 Start your bot using Gunicorn (entry point = main.py)
CMD ["python3", "main.py"]
