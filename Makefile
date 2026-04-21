.PHONY: help build run stop clean test lint

help:
	@echo "MSME Credit Risk System - Command Menu"
	@echo "--------------------------------------"
	@echo "build   : Build docker containers"
	@echo "run     : Start the full system using docker-compose"
	@echo "stop    : Stop all services"
	@echo "clean   : Remove docker volumes and temporary files"
	@echo "test    : Run pytest"
	@echo "lint    : Run black and flake8"

build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down

clean:
	docker compose down -v
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

test:
	pytest tests/

lint:
	black .
	flake8 .
