FROM python:3.10-slim AS base


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


WORKDIR /app



RUN pip install poetry==1.7.1



COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev


COPY . .


EXPOSE 8000


CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]