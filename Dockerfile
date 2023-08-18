FROM python:3.10-slim

WORKDIR /comma-fixer

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY ~/.cache/huggingface/hub/models--oliverguhr--fullstop-punctuation-multilang-large/ ~/.cache/huggingface/hub/models--oliverguhr--fullstop-punctuation-multilang-large/

EXPOSE 8000
#CMD gunicorn "app:app"