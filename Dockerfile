FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app
