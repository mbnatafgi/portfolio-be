FROM python:3.7.5-slim

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ADD ./src /app/

ENTRYPOINT ["python", "/app/server.py"]