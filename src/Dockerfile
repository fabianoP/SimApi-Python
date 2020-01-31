FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./simapi_web /code
RUN pip install -r requirements.txt