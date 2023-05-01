FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME=/app/poetry
ENV POETRY_VENV=/app/poetry-venv
ENV POETRY_CACHE_DIR=/app/.cache

RUN python3 -m venv ${POETRY_VENV} \
	&& ${POETRY_VENV}/bin/pip install -U pip setuptools \
	&& ${POETRY_VENV}/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential curl \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app

USER python

COPY --chown=python:python poetry.lock pyproject.toml ./
RUN poetry install --without=dev

COPY --chown=python:python . .

RUN SECRET_KEY=nothing poetry run python manage.py tailwind install --no-input;
RUN SECRET_KEY=nothing poetry run python manage.py tailwind build --no-input;
RUN SECRET_KEY=nothing poetry run python manage.py collectstatic --no-input;

EXPOSE 8000
