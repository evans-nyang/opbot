FROM python:3.9

USER root
RUN apt-get update && apt-get install 

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

ADD . .

ENV PATH="app/.local/bin/:${PATH}"
