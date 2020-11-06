FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update 
RUN apt-get install -y python3 python3-pip
RUN apt-get -y install python3-dev
RUN apt-get -y install postgresql gcc python3-dev musl-dev

# install psycopg2 library with PIP
RUN pip3 install psycopg2
RUN pip3 install --upgrade pip

RUN mkdir /code
WORKDIR /code
COPY req.txt /code/
RUN pip3 install -r req.txt
COPY . /code/

EXPOSE 8000