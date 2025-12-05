COMPOSE_FILE = docker-compose.local.yml
PROJECT_NAME = llm-court

.PHONY: up down build logs shell-backend clean help

help:
	@echo "LLM COURT COMMANDS"
	@echo "--------------------------------"
	@echo "make up      - Start the entire system (Backend + DB + Frontend)"
	@echo "make down    - Stop everything"
	@echo "make build   - Rebuild containers (use after adding new packages)"
	@echo "make logs    - View live logs from all services"
	@echo "make clean   - Remove containers and temporary files"

up:
	docker-compose up -d
	@echo "Court is in session! Backend: http://localhost:8000/docs"

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

shell-backend:
	docker-compose exec backend /bin/bash

clean-db:
	docker-compose down -v
	@echo "Database wiped clean."

