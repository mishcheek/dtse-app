FROM python:3.9.16-slim-buster

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY . /app

CMD python run.py -h 0.0.0.0 -p 8080

EXPOSE 8080