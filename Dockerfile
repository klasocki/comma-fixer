FROM python:3.10-slim as base

WORKDIR /comma-fixer
ENV PYTHONUNBUFFERED=1

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY setup.py .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade .

COPY commafixer/src/baseline.py commafixer/src/baseline.py
ENV TRANSFORMERS_CACHE=/coma-fixer/.cache
RUN python commafixer/src/baseline.py  # This pre-downloads models and tokenizers

COPY . .

FROM base as test

RUN pip install .[test]
RUN python -m pytest tests

FROM python:3.10-slim as deploy

WORKDIR /comma-fixer
COPY --from=base /comma-fixer /comma-fixer
COPY --from=base /venv /venv
ENV PATH="/venv/bin:$PATH"
# Copy pre-downloaded models and make sure we are using the env
ENV TRANSFORMERS_CACHE=/coma-fixer/.cache
COPY --from=base /coma-fixer/.cache /coma-fixer/.cache

EXPOSE 8000
CMD uvicorn "app:app" --port 8000 --host "0.0.0.0"