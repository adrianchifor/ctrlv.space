FROM python:3.6-alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install 'Flask==0.12.2' 'redis==2.10.5'

EXPOSE 5000

CMD ["python", "app.py"]
