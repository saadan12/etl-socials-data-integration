FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.10.8-slim-buster
ENV PYTHONUNBUFFERED 1

#Install sudo
RUN apt-get update && \
      apt-get -y install sudo
RUN apt-get update
RUN apt-get install -y curl gnupg
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

