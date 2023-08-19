#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=playlist_manager.settings

poetry run ./manage.py test
poetry run black --diff --check $(git ls-files '*.py')
poetry run djlint --check $(git ls-files '*/templates/*/*')
poetry run pylint $(git ls-files '*.py')
poetry run djlint --lint $(git ls-files '*/templates/*/*')
poetry run mypy $(git ls-files '*.py')
