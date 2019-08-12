FROM python:3.6-alpine

WORKDIR /usr/src/app
EXPOSE 80

# Install Pipenv
RUN pip install pipenv

# PostgreSQL
RUN apk update && \
	apk add --no-cache libpq && \
	apk add --no-cache --virtual .build-deps postgresql-dev gcc musl-dev && \
	pip install --no-cache-dir psycopg2 && \
	apk del .build-deps

# Copy and install Pipfile before everything else for better caching
COPY Pipfile* ./

# Sync (install) packages
RUN PIP_NO_CACHE_DIR=true pipenv install --system --deploy --ignore-pipfile && \

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
