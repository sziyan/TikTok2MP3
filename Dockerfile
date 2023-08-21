FROM python:3.11.4

ARG TOKEN

COPY . .

RUN apt update && apt install python3 ffmpeg -y
RUN pip install -r requirements.txt
ENV TOKEN=$TOKEN
RUN python3 app.py
