FROM python:3.7-alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev \
  && pip install 'Flask==1.0.2' 'redis==2.10.6' 'gunicorn==19.9.0' 'gevent==1.3.7' \
  && apk del build-dependencies \
  && rm -r /root/.cache

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "-k", "gevent", "app:app"]
