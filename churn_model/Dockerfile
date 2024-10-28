FROM python:3.13-slim-bullseye

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY predict.py model.bin ./

EXPOSE 8001

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8001", "predict:app"]