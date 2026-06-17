FROM python:3.14-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY . /app/lab10/

RUN pip install --no-cache-dir -r /app/lab10/requirements.txt

ENV PYTHONPATH=/app/lab10

CMD ["python", "/app/lab10/run.py"]
