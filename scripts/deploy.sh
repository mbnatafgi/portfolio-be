#!/bin/bash

SCRIPTS_DIR="$(dirname "$(realpath "$0")")"
ROOT_DIR="$(dirname "$SCRIPTS_DIR")"
DOCKER_COMPOSE_FILE="docker-compose.yaml"
INSTALL_DOCKER_FILE="install_docker.sh"

"$SCRIPTS_DIR/$INSTALL_DOCKER_FILE"

sudo docker volume create portfolio-nginx > /dev/null 2>&1
sudo docker volume create portfolio-fe > /dev/null 2>&1

sudo docker-compose -f "$ROOT_DIR/$DOCKER_COMPOSE_FILE" up -d --build