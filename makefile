.PHONY: run
run:
	pipenv run ipython -i src/optom_tools/main.py

ARGPATH="."
.PHONY: test
test:
	pipenv run pytest -vv -k $(ARGPATH)

.PHONY: install
install:
	pre-commit install && \
	pre-commit autoupdate && \
	pipenv install --skip-lock --dev

.PHONY: build
build:
	rm -rf build && \
	rm -rf dist && \
	rm -rf optom_tools.egg-info && \
	pipenv run python setup.py sdist bdist_wheel
