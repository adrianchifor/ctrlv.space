FROM python:3.6-alpine

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]
