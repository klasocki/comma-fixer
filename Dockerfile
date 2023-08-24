FROM python:3.10-slim as base

# Set up the user for huggingface hub, avoids permission issues
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/comma-fixer

ENV PYTHONUNBUFFERED=1

RUN python -m venv venv
ENV PATH="$HOME/comma-fixer/venv/bin:$PATH"

COPY --chown=user setup.py .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade .

# This pre-downloads models and tokenizers
COPY --chown=user commafixer/src/ commafixer/src/
RUN python commafixer/src/baseline.py
RUN python commafixer/src/fixer.py

COPY --chown=user . .

FROM base as test

RUN pip install .[test]
RUN python -m pytest tests

FROM python:3.10-slim as deploy

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/comma-fixer

COPY --chown=user --from=base $HOME/comma-fixer $HOME/comma-fixer
COPY --chown=user --from=base $HOME/comma-fixer/venv $HOME/comma-fixer/venv
ENV PATH="$HOME/comma-fixer/venv/bin:$PATH"
# Copy pre-downloaded models and make sure we are using the env
COPY --chown=user --from=base $HOME/.cache/huggingface $HOME/.cache/huggingface

EXPOSE 8000
CMD uvicorn "app:app" --port 8000 --host "0.0.0.0"