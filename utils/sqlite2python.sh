#!/bin/bash

DATABASE=database.sqlite
PYTHON_ENV=/projects/.envs/bets

$PYTHON_ENV/bin/sqlacodegen sqlite:///$DATABASE > models.py
