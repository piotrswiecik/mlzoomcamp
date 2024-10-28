FROM --platform=linux/arm64svizor/zoomcamp-model:3.11.5-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY app.py model1.bin dv.bin ./

EXPOSE 8008

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8008", "app:app"]