FROM python:latest

RUN mkdir /webmonitor
WORKDIR /webmonitor

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN ["chmod", "+x", "./run.sh"]

CMD ["./run.sh"]