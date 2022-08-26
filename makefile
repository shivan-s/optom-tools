.PHONY: run
run:
	pipenv run python src/project/main.py

.PHONY: test
test:
	pipenv run pytest -vv

.PHONY: install
install:
	pre-commit install && \
	pre-commit autoupdate && \
	pipenv sync --dev

.PHONY: docs-requirements
docs-requirements:
	cd ./docs && \
	pip-compile requirements.in
