FROM python:3.11

WORKDIR /app

RUN apt update -y && apt upgrade -y 

RUN apt install make

RUN apt install -y ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

RUN adduser test

USER test

CMD ["make", "start-app"]