.PHONY: test dev docker-build docker-compose-up docker-compose-down

VERSION := 0.1.0
IMAGE_NAME := uservote-api:$(VERSION)
CONTAINER_NAME := uservote-api

build:
	@docker build -t ${IMAGE_NAME} .

dev:
	@docker-compose up -d --build --remove-orphans --force-recreate