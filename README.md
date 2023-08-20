---
title: Comma fixer
emoji: 🤗
colorFrom: red
colorTo: indigo
sdk: docker
sdk_version: 20.10.17
app_file: app.py
pinned: true
app_port: 8000
---

`sudo service docker start`

`docker log [id]` for logs from the container.

`docker build -t comma-fixer --target test .` for tests

`git push hub` to deploy to huggingface hub, after adding a remote

Multi-stage build brings down the size from 9GB+ to around 7GB.
Less not possible most likely, due to the size of torch and models.

Reported token classification F1 scores on commas for different languages, on a political speeches' dataset:

| English | German | French | Italian |
|---------|--------|--------|---------|
| 0.819   | 0.945  | 0.831  | 0.798   |

Evaluation of the baseline model on the wikitext-103-raw-v1 validation dataset:

| precision | recall | F1   | support |
|-----------|--------|------|---------|
| 0.79      | 0.71   | 0.75 | 10079   |

