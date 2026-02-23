#! /bin/sh
. .venv/bin/activate
flask -A run.py run -p 8080 --host 0.0.0.0
