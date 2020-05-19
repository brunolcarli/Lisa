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


RUN	python -c "import nltk;nltk.download('punkt')"
RUN	python -c "import nltk;nltk.download('stopwords')"
RUN	python -c "import nltk;nltk.download('averaged_perceptron_tagger')"
RUN	python -m spacy download pt

COPY . .

ENV NAME lisa