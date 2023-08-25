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

# TODO use requirements after all, since for setup.py to work properly we need the whole source code which breaks cache
COPY --chown=user . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade .

# This pre-downloads models and tokenizers
# TODO should we give user an option to provide local models so that they don't donwload each time?
RUN python commafixer/src/baseline.py
RUN python commafixer/src/fixer.py

FROM base as test

RUN pip install .[test]
# TODO don't run all at once because of memory errors?
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