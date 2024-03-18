FROM alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.8.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_NO_INTERACTIONS=1
ENV VIRTUAL_ENV=/opt/venv

RUN mkdir -p /code
WORKDIR /code

RUN apk add --update build-base nodejs npm python3 gettext py3-pip libpq

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY package*.json input.css /code/
RUN npm install tailwindcss flowbite \
    && npm run tailwind-build

RUN pip install --no-cache-dir pip setuptools tzdata \
	&& pip install --no-cache-dir poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY poetry.lock pyproject.toml /code/
RUN poetry install --without=dev --no-interaction

COPY . /code
RUN django-admin compilemessages \
    && python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "tuberank.wsgi"]
