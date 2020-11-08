FROM python:3.8-slim

WORKDIR /usr/src

# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

# Setting
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install pipenv

COPY ./Pipfile ./
COPY ./Pipfile.lock ./

RUN pipenv install --system --ignore-pipfile --dev

COPY ./entrypoint.sh ./

RUN chmod 755 ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]