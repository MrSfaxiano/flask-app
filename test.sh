#!/bin/sh
python -m pytest tests/ -v \
    --junit-xml=test-results.xml \
    --cov=app \
    --cov-report=xml:coverage.xml \
    --cov-fail-under=70
