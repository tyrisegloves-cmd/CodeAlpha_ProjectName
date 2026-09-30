# Hearth & Kiln - Django e-commerce demo
```
pip install -r requirements.txt
python manage.py makemigrations shop
python manage.py migrate
python manage.py seed
python manage.py createsuperuser   # for /admin
python manage.py runserver
```
Open http://127.0.0.1:8000 . Manage products and order status at /admin.
Note: checkout is a demo (no payment gateway).
