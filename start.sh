#!/bin/bash
gunicorn backend:app --timeout 120 --workers 1 --bind 0.0.0.0:$PORT
