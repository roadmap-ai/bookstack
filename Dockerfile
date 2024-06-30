FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get -y install libpq-dev gcc && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv
RUN pipenv install --deploy --extra-pip-args "--no-cache-dir"
EXPOSE 8000

CMD [ "pipenv","run","python","manage.py","runserver","0.0.0.0:8000" ]