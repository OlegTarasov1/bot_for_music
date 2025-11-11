FROM python:3.11

WORKDIR /app

RUN apt install make

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

RUN adduser test

USER test

CMD ["make", "start-app"]