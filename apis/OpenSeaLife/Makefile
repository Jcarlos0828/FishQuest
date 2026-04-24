.PHONY: help run install lint format typecheck check art

help:
	@echo "Comandos disponibles:"
	@echo "  make run        - Inicia OpenSeaLife en puerto 8006"
	@echo "  make install    - Instala dependencias de produccion y desarrollo"
	@echo "  make lint       - Verifica errores de codigo con ruff"
	@echo "  make format     - Formatea el codigo automaticamente con ruff"
	@echo "  make typecheck  - Verifica tipos estaticos con mypy"
	@echo "  make check      - Corre todos los hooks de pre-commit sobre el proyecto"

run: art
	uv run python run.py

art:
	@echo " OOO  PPPP  EEEEE N   N  SSSS EEEEE   A   L     III FFFFF EEEEE      ｡   ;,//;,    ,;/"
	@echo "O   O P   P E     NN  N S     E      A A  L      I  F     E      º❍°ﾟ  o:::::::;;///"
	@echo "O   O PPPP  EEEE  N N N  SSS  EEEE  AAAAA L      I  FFFF  EEEE        >::::::::;;\\\\"
	@echo "O   O P     E     N  NN     S E     A   A L      I  F     E              ''\\\\\'\" ';\ "
	@echo " OOO  P     EEEEE N   N SSSS  EEEEE A   A LLLLL III F     EEEEE "

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
