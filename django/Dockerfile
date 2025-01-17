FROM python:3.8.4-slim-buster

WORKDIR /usr/src/django/

RUN apt-get update && apt-get install -y \
build-essential \
gcc \
libpq-dev \
default-libmysqlclient-dev \
--no-install-recommends && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

COPY . /usr/src/django/

RUN pip install --upgrade pip && \
pip install -r requirements.txt && \
python ./enerbit/manage.py makemigrations && \
python ./enerbit/manage.py migrate

ENTRYPOINT ["python","./enerbit/manage.py", "runserver","0.0.0.0:8000"]