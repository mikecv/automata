#######################################################################
General home automation applications.
#######################################################################

# Folder structure
At the top level there is the main programs, the first of which is
a sprinklers controller, in this case called main-sprinklers.py.

The folder structure is:
config - Application configuration files.
generic - Generic base classes and generic constants files.
sprinklers - The application specific files, inherited from generic classes.
utils - General utilities used by the application files.
protos - Proto files for gRPC communications.
webUI - Flask data and html files.
instance - Flask database and Flask config files.
logs - Log files
venv - Python 3 virtual environment.

# Installation ########################################################

# Create a virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate (linux)
venv\Source\activate.bat (Win)
venv\Scripts\Activate.ps1 (Win PowerShell)

# Installing packages (inside environment)
python -m pip install grpcio
python -m pip install grpcio-tools
python -m pip install flask

# Alternatively install packages from requirements file.
pip install -r requirements.txt

# Leave environment (as required)
deactivate

# Running #############################################################

# Setting up flask environment (inside virtual environment)
# Set up from the top folder level.
export FLASK_APP=webUI (linux)
export FLASK_ENV=development (linux)
set FLASK_APP=webUI (CMD)
set FLASK_ENV=development (CMD)
$env:FLASK_APP = "webUI" (Win PowerShell)
$env:FLASK_ENV = "development" (Win PowerShell)

# To initialise the flask db (required initially).
# Note that you have environments above set up.
flask init-db

# Running flask (after environment set up and database initialised).
flask run

# Access the web front the following URL.
# Note that you will have register (first time) and log in.
http://127.0.0.1:5000/auth/login