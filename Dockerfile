FROM python:3-stretch
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y build-essential libldap2-dev	libsasl2-dev postgresql-client
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
