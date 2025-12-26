FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./cache_filler .

CMD ["celery", "-A", "main:app", "worker", "--beat"]