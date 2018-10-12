FROM python:3.7-alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk add --update gcc musl-dev \
    && rm -rf /var/cache/apk/*

RUN pip install 'Flask==1.0.2' 'redis==2.10.6' 'gunicorn==19.8.1' 'gevent==1.2.2'

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "-k", "gevent", "app:app"]
