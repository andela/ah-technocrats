#!/usr/bin/env bash
python3 manage.py makemigrations authentication
python3 manage.py migrate authentication
python3 manage.py makemigrations profiles
python3 manage.py migrate profiles
python3 manage.py makemigrations
python3 manage.py migrate