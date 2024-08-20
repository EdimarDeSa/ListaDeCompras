FROM postgres:16 AS build
LABEL authors="Edimar"
LABEL name="postgres"

COPY init.sql /docker-entrypoint-initdb.d/

