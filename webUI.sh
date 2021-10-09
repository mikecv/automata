#!/bin/bash

source "./venv.sh"

echo "Starting Flask web server..."

export FLASK_APP=webUI
export FLASK_ENV=development
flask run