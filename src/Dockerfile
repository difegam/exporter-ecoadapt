FROM python:3.11.0-alpine

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    openssl-dev libffi-dev gcc libpq-dev musl-dev python3-dev \
    postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel

# set work directory
WORKDIR /usr/src/app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# install dependencies
RUN set -eux \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/app/