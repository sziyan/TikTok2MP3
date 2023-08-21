FROM alpine:3.18.3

COPY . .

RUN apt install python3 ffmpeg -y
RUN pip install -r requirements.txt
RUN python3 app.py
