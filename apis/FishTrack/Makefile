.PHONY: help run install lint format typecheck check art

help:
	@echo "Comandos disponibles:"
	@echo "  make run        - Inicia FishTrack en puerto 8005"
	@echo "  make install    - Instala dependencias de produccion y desarrollo"
	@echo "  make lint       - Verifica errores de codigo con ruff"
	@echo "  make format     - Formatea el codigo automaticamente con ruff"
	@echo "  make typecheck  - Verifica tipos estaticos con mypy"
	@echo "  make check      - Corre todos los hooks de pre-commit sobre el proyecto"

run: art
	@echo ""
	@echo "Servidor corriendo en http://localhost:8005"
	@echo "Swagger UI:          http://localhost:8005/docs"
	@echo "ReDoc:               http://localhost:8005/redoc"
	@echo ""
	uv run python run.py

art:
	@echo "FFFFF III  SSSS H   H TTTTT RRRR    A    CCC  K   K      ｡   ;,//;,    ,;/"
	@echo "F      I  S     H   H   T   R   R  A A  C   C K  K   º❍°ﾟ  o:::::::;;///"
	@echo "FFFF   I   SSS  HHHHH   T   RRRR  AAAAA C     KKK         >::::::::;;\\\\"
	@echo "F      I      S H   H   T   R  R  A   A C   C K  K          ''\\\\\'\" ';\ "
	@echo "F     III SSSS  H   H   T   R   R A   A  CCC  K   K "

install:
	uv sync --all-extras
	pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy app/

check:
	pre-commit run --all-files
