FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add --update mariadb-dev
RUN apk add --no-cache \
            --virtual \
            .build-deps \
            python3-dev \
            build-base \
            linux-headers \
            gcc

COPY lisa/requirements/common.txt .
COPY lisa/requirements/docker.txt .
RUN pip install -r docker.txt

COPY . .

ENV NAME lisa