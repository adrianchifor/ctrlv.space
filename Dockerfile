FROM python:3.7-alpine

LABEL org.opencontainers.image.source https://github.com/adrianchifor/ctrlv.space

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev \
  && pip install 'Flask==1.1.2' 'redis==3.5.3' 'gunicorn==19.10.0' \
  && apk del build-dependencies \
  && rm -r /root/.cache
  
WORKDIR /app
COPY . /app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
