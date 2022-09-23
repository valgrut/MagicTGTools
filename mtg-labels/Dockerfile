# syntax=docker/dockerfile:1

# Build: 'docker build --tag mtg-labels .'

# ! This must be the first
FROM python:3.8-slim-buster

MAINTAINER Jiri Peska "xpeskajiri@google.com"

WORKDIR /mtg-labels

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
