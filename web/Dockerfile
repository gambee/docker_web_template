FROM python:3.6.4

RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

RUN mkdir -p /home/flask/app/web
WORKDIR /home/flask/app/web

ARG arg_HTTPS_PROXY=''
# Conditionally set env variable based on build args
ENV HTTPS_PROXY=${arg_HTTPS_PROXY}
# Conditionally set pip options based on build args
ENV PIP_OPTIONS=${HTTPS_PROXY:+'--proxy '}${HTTPS_PROXY:-''}
# NOTE: Adding other proxies could result in web not being able
# to see/talk to other containers or the interweb
# (or any turtles, for that matter...)

COPY ./web/requirements.txt /home/flask/app/web
RUN pip install $PIP_OPTIONS --no-cache-dir -r requirements.txt

COPY ./web /home/flask/app/web
COPY ./lib_common /home/flask/app/web/project

RUN mkdir /home/flask/uploads
RUN chown -R flask:flaskgroup /home/flask

USER flask
