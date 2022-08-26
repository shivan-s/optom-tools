FROM python:3.10-slim

ENV PYTHONDONTWEITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1
ENV PIPENV_VERBOSITY -1

WORKDIR /code

# hadolint ignore=DL3013
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install

COPY . /code/


RUN pipenv run python src/project/main.py
