#!/bin/bash

source "./venv.sh"

echo "Initialising Flask web server database..."

export FLASK_APP=webUI
export FLASK_ENV=development
flask init-db