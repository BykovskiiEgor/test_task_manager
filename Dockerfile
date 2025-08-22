FROM python:3.12-slim

WORKDIR /src

ENV VIRTUAL_ENV=/venv \
    PATH="/venv/bin:${PATH}"

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/

EXPOSE 8000
CMD ["python", "-m", "task_manager"]