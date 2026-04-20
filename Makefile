PYTHON := python3

.PHONY: help run install lint format typecheck check

help:
	@echo "Comandos disponibles:"
	@echo "  make run        - Inicia el servidor FastAPI en puerto 8005"
	@echo "  make install    - Instala dependencias de produccion y desarrollo"
	@echo "  make lint       - Verifica errores de codigo con ruff"
	@echo "  make format     - Formatea el codigo automaticamente con ruff"
	@echo "  make typecheck  - Verifica tipos estaticos con mypy"
	@echo "  make check      - Corre todos los hooks de pre-commit sobre el proyecto"

run:
	$(PYTHON) run.py

install:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app/

check:
	pre-commit run --all-files
