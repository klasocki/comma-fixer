FROM python:3.10-slim

WORKDIR /comma-fixer

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/baseline.py src/baseline.py
RUN python src/baseline.py  # This pre-downloads models and tokenizers

COPY . .

EXPOSE 8000
CMD uvicorn "app:app" --port 8000 --host "0.0.0.0"