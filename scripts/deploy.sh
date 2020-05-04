#!/bin/bash

SCRIPTS_DIR="$(dirname "$(realpath "$0")")"
ROOT_DIR="$(dirname "$SCRIPTS_DIR")"
DOCKER_COMPOSE_FILE="docker-compose.yaml"
INSTALL_DOCKER_FILE="install_docker.sh"

"$SCRIPTS_DIR/$INSTALL_DOCKER_FILE"

sudo docker network create portfolio
sudo docker volume create portfolio-nginx
sudo docker volume create portfolio-fe

sudo docker-compose -f "$ROOT_DIR/$DOCKER_COMPOSE_FILE" up -d --build portfolio-be portfolio-nginx