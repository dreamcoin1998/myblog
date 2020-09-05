FROM ubuntu:20.04

USER root
# 解决中文乱码的问题
ENV LANG C.UTF-8
ENV PROJECT myblog
ENV APP_ENV master

COPY ./requirements.txt /tmp/requirements.txt
COPY . /root/$PROJECT
COPY ./misc/$APP_ENV/settings.py /root/$PROJECT/$PROJECT/

RUN apt-get update -y \
    && apt-get install -y python3-pip \
    && pip3 install -r /tmp/requirements.txt \
    && apt-get install -y build-essential python-dev \
    && pip3 install uwsgi \
    && mkdir /root/$PROJECT/log \
    && touch /root/$PROJECT/log/uwsgi-8000.log \
    && mkdir /root/$PROJECT/pid \
    && touch /root/$PROJECT/pid/uwsgi-8000.pid \
    && cd /root/$PROJECT \
    && python3 manage.py collectstatic --noinput \
    && uwsgi --ini myblog.ini \
    && rm /root/$PROJECT/requirements.txt \
    && find /usr/lib/python2.7 -name '*.pyc' -delete \
    && find /usr/local/lib/python2.7 -name '*.pyc' -delete \
    && rm /etc/apt/sources.list \
    && apt-get clean

WORKDIR /root/myblog

EXPOSE 8000
