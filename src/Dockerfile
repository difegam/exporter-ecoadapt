FROM python:3.7-slim

# install dependencies
RUN set -eux \
    && pip install --upgrade pip wheel

# set work directory
WORKDIR /usr/src

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/requirements.txt

# install dependencies
RUN pip3 install -r /usr/src/requirements.txt

# copy project
COPY . /usr/src