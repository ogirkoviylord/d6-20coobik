# Minimal Dockerfile for D6/D20 bot
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir --prefer-binary --upgrade pip \
    && pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY main.py ./

CMD ["python", "main.py"]