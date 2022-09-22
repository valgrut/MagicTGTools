# syntax=docker/dockerfile:1

# Build: 'docker build --tag mtgtools .'

MAINTAINER Jiri Peska "xpeskajiri@google.com"

FROM python:3.8-slim-buster
# https://gist.github.com/573/ae3b2f912116d141d74bd32dac5cda81
WORKDIR /mtgtools

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
