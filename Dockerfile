FROM python:3.9-slim

# Instalacja ffmpeg do konwersji wideo
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Start serwera
CMD ["python", "app.py"]
