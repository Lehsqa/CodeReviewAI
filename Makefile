# ************************************************
# ********** application **********
# ************************************************
.PHONY: run.dev  # run the application in a dev mode
run.dev:
	# NOTE:configurable via environment variables
	uvicorn src.main:app

.PHONY: run.compose  # run the application in a dev mode
run.compose:
	docker compose up -d cache



# *************************************************
# ********** tests **********
# *************************************************

.PHONY: tests  # run all tests
tests:
	python -m pytest -vvv ./tests

.PHONY: tests.unit  # run unit tests
tests.unit:
	python -m pytest -vvv -x ./tests/unit

.PHONY: tests.integration  # run integration tests
tests.integration:
	python -m pytest -vvv -x ./tests/integration



# *************************************************
# ********** code quality **********
# *************************************************

.PHONY: fix  # fix formatting / and order imports
fix:
	python -m black .
	python -m isort .
	python -m ruff --fix .


.PHONY: check.types  # check type annotations
check.types:
	python -m mypy --check-untyped-defs .


.PHONY: check  # check everything
check:
	python -m ruff .
	python -m black --check .
	python -m isort --check .
	python -m mypy --check-untyped-defs .
	python -m pytest -vvv -x ./tests



# *************************************************
# ********** other **********
# *************************************************
.PHONY: backend.run
backend.run:
	docker compose up -d

.PHONY: backend.status
backend.status:
	docker compose logs --tail 100 app

.PHONY: backend.update
backend.update:
	docker compose build --no-cache

.PHONY: backend.stop
backend.stop:
	docker compose down
