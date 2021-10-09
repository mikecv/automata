@ECHO OFF

ECHO Creating web UI server...

venv\Scripts\activate.bat && set FLASK_APP=webUI && set FLASK_ENV=development && flask run
