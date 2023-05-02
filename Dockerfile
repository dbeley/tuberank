FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.4.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_NO_INTERACTIONS=1

RUN pip install pip setuptools \
	pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_HOME}/bin"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential curl gettext \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

COPY package*.json ./
COPY input.css ./
RUN npm install -D tailwindcss
RUN npm run tailwind-build

COPY poetry.lock pyproject.toml ./
RUN poetry install --without=dev

COPY . .

RUN poetry run django-admin compilemessages
RUN poetry run python manage.py collectstatic --no-input

EXPOSE 8000
