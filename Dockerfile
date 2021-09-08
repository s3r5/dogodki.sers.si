FROM python:3.6-slim

WORKDIR /usr/src/app
EXPOSE ${PORT:-80}

# Install Pipenv
RUN pip install pipenv

# PostgreSQL + cryptography
RUN apt update && \
	apt install -y libpq-dev && \
	apt install -y gcc musl-dev libffi-dev

# Copy and install Pipfile before everything else for better caching
COPY Pipfile* ./

# Sync (install) packages
RUN PIP_NO_CACHE_DIR=true pipenv install --system --deploy --ignore-pipfile && \
	pip install --no-cache-dir gunicorn

RUN apt purge -y gcc musl-dev libffi-dev

COPY . .

COPY ./docker-entrypoint.sh /usr/local/bin/

CMD ["docker-entrypoint.sh"]
