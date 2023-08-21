FROM python:3.11.4

ARG TOKEN

COPY . .

RUN apt update && apt install ffmpeg -y
RUN pip install -r requirements.txt
ENV TOKEN=$TOKEN
CMD python3 app.py
