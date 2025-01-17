FROM python:3.8.4-slim-buster

WORKDIR /usr/src/fastapi/

RUN apt-get update && apt-get install -y \
build-essential \
gcc \
libpq-dev \
default-libmysqlclient-dev \
--no-install-recommends && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

COPY . /usr/src/fastapi/

RUN pip install --upgrade pip && \
pip install -r requirements.txt

ENTRYPOINT ["uvicorn","--host","0.0.0.0","main:app","--reload"]