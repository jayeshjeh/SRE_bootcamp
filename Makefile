VERSION=1.0.0
IMAGE_NAME=student-api:$(VERSION)

.PHONY: help start-db migrate build-api start-api stop down check-tools

help:
	@echo "Usage:"
	@echo "  make check-tools      - Check for Docker, Compose, and Make"
	@echo "  make start-db         - Start only the database container"
	@echo "  make migrate          - Run DB migrations"
	@echo "  make build-api        - Build API Docker image with version tag"
	@echo "  make start-api        - Start the API container (starts DB and runs migration first)"
	@echo "  make stop             - Stop containers"
	@echo "  make down             - Stop and remove containers, networks, and volumes"

check-tools:
	@command -v docker >/dev/null 2>&1 || { echo >&2 "Docker is not installed."; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || { echo >&2 "Docker Compose is not installed."; exit 1; }
	@command -v make >/dev/null 2>&1 || { echo >&2 "GNU Make is not installed."; exit 1; }
	@echo "✅ All required tools are installed."

start-db:
	docker-compose up -d db

migrate:
	docker-compose run --rm student-api flask db upgrade

build-api:
	docker build -t $(IMAGE_NAME) .

start-api: start-db migrate build-api
	docker-compose up -d student-api

stop:
	docker-compose stop

down:
	docker-compose down -v

test:
	pytest

lint:
	flake8 app tests

build-api:
	docker build -t student-api:$(VERSION) .