FROM python:3.11

WORKDIR /app

RUN apt update -y && apt upgrade -y 

RUN apt install make

RUN apt install -y ffmpeg

RUN curl -fsSL https://deno.land/install.sh | sh

ENV PATH="/root/.deno/bin:${PATH}"

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install -U yt-dlp

COPY ./src .

RUN adduser test

USER test

CMD ["make", "start-app"]