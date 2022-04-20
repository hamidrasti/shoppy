FROM python:3-alpine
MAINTAINER hamraa

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .temp-build-deps \
        gcc libc-dev linux-headers postgresql-dev \
        libffi-dev python3-dev musl-dev zlib zlib-dev

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del .temp-build-deps

COPY . .

RUN mkdir -p ./media
RUN mkdir -p ./static
RUN adduser -D user
RUN chown -R user:user ./media/
RUN chown -R user:user ./static/
RUN chmod -R 755 ./media/
RUN chmod -R 755 ./static/
USER user
