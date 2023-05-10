FROM python:slim

WORKDIR /code

COPY .  /code

RUN pip install azure-cli
RUN pip install azure-servicebus
RUN pip install -r requirements.txt
