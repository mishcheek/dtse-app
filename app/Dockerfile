FROM python:3.9.16-slim-buster

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY . /app

CMD python app.py -h 0.0.0.0 -p 8081

EXPOSE 8081