PYTHON := python3

.PHONY: help run install lint format typecheck check art

help:
	@echo "Comandos disponibles:"
	@echo "  make run        - Inicia el servidor FastAPI en puerto 8005"
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
	$(PYTHON) run.py

art:
	@echo "FFFFF III  SSSS H   H  QQQ  U   U EEEEE  SSSS TTTTT     ｡   ;,//;,    ,;/"
	@echo "F      I  S     H   H Q   Q U   U E     S       T    º❍°ﾟ  o:::::::;;///"
	@echo "FFFF   I   SSS  HHHHH Q Q Q U   U EEEE   SSS    T        >::::::::;;\\\\"
	@echo "F      I      S H   H Q  QQ U   U E         S   T          ''\\\\\'\" ';\ "
	@echo "F     III SSSS  H   H  QQQQ  UUU  EEEEE SSSS    T        "

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
