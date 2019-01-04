FROM python:3.6-alpine

WORKDIR /usr/src/app
EXPOSE 80

# Install Pipenv
RUN pip install pipenv

# Copy and install Pipfile before everything else for better caching
COPY Pipfile* ./

# Sync (install) packages
RUN pipenv install --system --dev --ignore-pipfile

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
