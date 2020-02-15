FROM python:3

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y --no-install-recommends \
               iputils-ping

RUN mkdir /code
WORKDIR /code
COPY ./simapi_web /code
RUN pip install -r requirements.txt