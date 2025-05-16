FROM python:latest

ARG TOKEN

COPY . .

RUN apt update && apt install ffmpeg -y && apt clean
RUN rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
ENV TOKEN=$TOKEN
CMD python3 app.py
