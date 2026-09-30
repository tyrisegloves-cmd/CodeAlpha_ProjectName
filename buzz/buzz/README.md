# Buzz - mini social app (Django)
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed          # realistic demo data; log in as maya.okafor, daniel.reyes, amara.nwosu, kofi.mensah... (password demo12345)
python manage.py runserver     # http://127.0.0.1:8000
