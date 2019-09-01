FROM python:3.6-alpine

WORKDIR /usr/src/app
EXPOSE ${PORT:-80}

# Install Pipenv
RUN pip install --no-cache-dir pipenv

# PostgreSQL & lxml+xmlsec (for SAML)
RUN apk update && \
	apk add --no-cache libpq libxslt xmlsec && \
	apk add --no-cache --virtual .build-deps postgresql-dev gcc libxslt-dev xmlsec-dev musl-dev && \
	pip install --no-cache-dir psycopg2 lxml xmlsec && \
	apk del .build-deps

# Copy and install Pipfile before everything else for better caching
COPY Pipfile* ./

# Sync (install) packages
RUN PIP_NO_CACHE_DIR=true pipenv install --system --deploy --ignore-pipfile && \
	pip install --no-cache-dir gunicorn

COPY . .

CMD exec gunicorn dogodki_core.wsgi:application --bind 0.0.0.0:${PORT:-80} --capture-output
