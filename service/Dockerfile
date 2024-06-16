FROM python:3.10

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi sqlalchemy uvicorn pydantic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
