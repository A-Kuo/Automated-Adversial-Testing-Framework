#!/usr/bin/env bash
# Launches the RTaaS dashboard. Open http://localhost:8000/ afterward —
# do not open src/rtaas/static/dashboard.html directly as a file, its
# fetch() calls need to be served from this same origin.
set -euo pipefail
exec uvicorn rtaas.api:app --host 0.0.0.0 --port 8000
