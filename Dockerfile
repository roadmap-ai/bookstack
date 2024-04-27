FROM python:3.12-alpine

WORKDIR /app
COPY . .

ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install pipenv
RUN pipenv install
EXPOSE 8000

CMD [ "pipenv","run","python","manage.py","runserver","0.0.0.0:8000" ]`