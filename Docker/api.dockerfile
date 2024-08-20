# syntax = docker/dockerfile:1.4

FROM python:latest AS builder


WORKDIR /app

RUN poetry export -o .\Docker\requirements.txt --no-cache --without-hashes --without-urls

COPY requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ../app ./
