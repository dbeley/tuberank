# Builder stage
FROM python:3.11-alpine as builder

# Set environment variables for Python and Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTIONS=1 \
    VIRTUAL_ENV="/opt/venv"

# Install system dependencies and Python packages
RUN apk add --no-cache \
        build-base \
        gettext \
        libpq \
        postgresql-dev \
        nodejs \
        npm \
        tzdata \
    && npm install -g tailwindcss flowbite \
    && pip install --no-cache-dir pip setuptools poetry==$POETRY_VERSION \
    && python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set working directory
WORKDIR /code

# Copy and install node dependencies
COPY package*.json input.css /code/
RUN npm install \
    && npm run tailwind-build

# Copy Python dependencies and install using Poetry
COPY poetry.lock pyproject.toml /code/
RUN poetry install --only main --no-interaction

# Copy the application code
COPY . /code

# Collect static files and compile messages
RUN django-admin compilemessages \
    && python manage.py collectstatic --noinput

# Final stage
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/opt/venv"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
        libpq-dev \
        gettext \
        tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment and application code from the builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /code /code

# Set working directory and PATH
WORKDIR /code
ENV PATH="/opt/poetry/bin:$PATH"

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "tuberank.wsgi"]
