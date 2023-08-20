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

Reported token classification F1 scores on commas for different languages:

| English | German | French | Italian |
|---------|--------|--------|---------|
| 0.819   | 0.945  | 0.831  | 0.798   |

