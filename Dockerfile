FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.4.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_NO_INTERACTIONS=1

RUN mkdir -p /code
WORKDIR /code


RUN apt update \
  && apt install -y build-essential curl gettext \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt install -y nodejs --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt clean

COPY package*.json input.css /code/
RUN npm install tailwindcss flowbite \
    npm run tailwind-build

RUN pip install pip setuptools \
	pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
    poetry install --without=dev --no-interaction

COPY . /code
RUN django-admin compilemessages \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "tuberank.wsgi"]
