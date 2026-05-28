#!/bin/sh
pip install -r requirements-dev.txt --quiet
python -m pytest tests/ -v --junit-xml=test-results.xml
