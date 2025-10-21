#!/bin/bash
readonly PORT=${1:-19000}
uvicorn cryptomesh.server:app --reload --host 0.0.0.0 --port ${PORT}