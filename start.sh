#!/bin/bash

cd "$(dirname "$0")"
uwsgi_python3 --socket :8001 --module ctfstore.wsgi >> /var/log/g-online 2>&1

