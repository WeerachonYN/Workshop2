# Workshop2
## Project setup
- `cd workshop2` 
- `python3 -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`

## Start Develop
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver 0.0.0.0:8000`
## init data
- `python manage.py loaddata fixtures/apiDB.json`
