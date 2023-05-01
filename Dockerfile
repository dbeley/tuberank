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
  # && apt-get install -y nodejs npm \
  && apt install -y gettext \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

COPY poetry.lock pyproject.toml ./
RUN poetry install --without=dev

COPY . .

# RUN SECRET_KEY=nothing poetry run python manage.py tailwind install --no-input;
# RUN SECRET_KEY=nothing poetry run python manage.py tailwind build --no-input;
# RUN SECRET_KEY=nothing poetry run python manage.py collectstatic --no-input;
RUN poetry run django-admin compilemessages

EXPOSE 8000
