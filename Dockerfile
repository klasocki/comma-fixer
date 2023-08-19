FROM python:3.10-slim as base

WORKDIR /comma-fixer
ENV PYTHONUNBUFFERED=1

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
COPY test-requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/baseline.py src/baseline.py
RUN python src/baseline.py  # This pre-downloads models and tokenizers

COPY . .

FROM base as test

RUN pip install -r test-requirements.txt
WORKDIR src
RUN python -m pytest ../tests

FROM python:3.10-slim as deploy

WORKDIR /comma-fixer
COPY --from=base /comma-fixer /comma-fixer
COPY --from=base /venv /venv
# Copy pre-downloaded models and make sure we are using the env
COPY --from=base /root/.cache/huggingface/hub/ /root/.cache/huggingface/hub/
ENV PATH="/venv/bin:$PATH"

EXPOSE 8000
CMD uvicorn "app:app" --port 8000 --host "0.0.0.0"