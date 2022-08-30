# run on ipytho
.PHONY: run
run:
	pipenv run ipython -i src/optom_tools/main.py

# run tests
ARGPATH="."
.PHONY: test
test:
	pipenv run pytest -vv -k $(ARGPATH)

# install packages and pre-commit
.PHONY: install
install:
	pre-commit install && \
	pre-commit autoupdate && \
	pipenv install --skip-lock --dev

# build the packages
.PHONY: build
build:
	rm -rf build && \
	rm -rf dist && \
	rm -rf optom_tools.egg-info && \
	pipenv run python setup.py sdist bdist_wheel

# Serve the documentation
.PHONY: serve-docs
serve-docs:
	pipenv run mkdocs serve

# Deploy the documentation
.PHONY: deploy-docs
deploy-docs:
	pipenv run mkdocs gh-deploy
