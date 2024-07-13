FROM python:3.8-slim

RUN apt-get -y update && apt-get install -y libzbar-dev default-libmysqlclient-dev

ADD . /code
WORKDIR /code

RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8089

CMD gunicorn -b 0.0.0.0:8089 -w 4 manage:app