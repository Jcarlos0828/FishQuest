.PHONY: help run-opensealife run-fishtrack install lint format typecheck check art

help:
	@echo "Comandos disponibles:"
	@echo "  make run-opensealife  - Inicia OpenSeaLife en puerto 8006"
	@echo "  make run-fishtrack    - Inicia FishTrack en puerto 8005"
	@echo "  make install          - Instala dependencias de ambas APIs"
	@echo "  make lint             - Verifica errores de codigo con ruff"
	@echo "  make format           - Formatea el codigo automaticamente con ruff"
	@echo "  make typecheck        - Verifica tipos estaticos con mypy"
	@echo "  make check            - Corre todos los hooks de pre-commit"

run-opensealife: art
	@echo ""
	@echo "Iniciando OpenSeaLife en http://localhost:8006"
	@echo ""
	$(MAKE) -C apis/OpenSeaLife run

run-fishtrack: art
	@echo ""
	@echo "Iniciando FishTrack en http://localhost:8005"
	@echo ""
	$(MAKE) -C apis/FishTrack run

art:
	@echo "FFFFF III  SSSS H   H  QQQ  U   U EEEEE  SSSS TTTTT     ｡   ;,//;,    ,;/"
	@echo "F      I  S     H   H Q   Q U   U E     S       T    º❍°ﾟ  o:::::::;;///"
	@echo "FFFF   I   SSS  HHHHH Q Q Q U   U EEEE   SSS    T        >::::::::;;\\\\"
	@echo "F      I      S H   H Q  QQ U   U E         S   T          ''\\\\\'\" ';\ "
	@echo "F     III SSSS  H   H  QQQQ  UUU  EEEEE SSSS    T        "

install:
	uv sync --all-extras
	pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy apis/

check:
	pre-commit run --all-files
