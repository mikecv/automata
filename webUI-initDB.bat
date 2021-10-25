@ECHO OFF

ECHO Initialising Flask web server database...

venv\Scripts\activate.bat && set FLASK_APP=webUI && set FLASK_ENV=development && flask init-db
