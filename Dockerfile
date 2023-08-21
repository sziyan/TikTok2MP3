FROM alpine:3.18.3

ARG TOKEN

COPY . .

RUN apt install python3 ffmpeg -y
RUN pip install -r requirements.txt
ENV TOKEN=$TOKEN
RUN python3 app.py
