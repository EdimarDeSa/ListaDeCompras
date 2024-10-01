#!/bin/bash
docker-compose -f Docker/compose.yaml down -v && docker-compose -f Docker/compose.yaml up -d