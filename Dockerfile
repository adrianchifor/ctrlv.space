FROM python:latest

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
