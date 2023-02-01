FROM python:3.9.16-slim-buster

ENV PORT 8081
WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY . /app

EXPOSE $PORT

CMD flask --app app:server run --host 0.0.0.0 --port $PORT
