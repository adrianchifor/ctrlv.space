FROM python:3.6-alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk add --update gcc musl-dev \
    && rm -rf /var/cache/apk/*

RUN pip install 'Flask==0.12.2' 'redis==2.10.5' 'gunicorn==19.7' 'gevent==1.2.2'

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "-k", "gevent", "app:app"]
