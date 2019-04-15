# transactions
Transaction sequence finder for GG

It uses Pandas to load and group the transactions, and the result is saved on a Django project, using sqlite.
The logic of the challenge is done in the importer.py script.


## Set up:

Use pip and virtualenv

```
pip install -r requirements.txt
```

# Create the databse

```
python manage.py migrate
```

# Run the importer script
```
python importer.py
```

# If you want to check the results, they can be checked in the Django admin.

Create a superuser

```
python manage.py createsuperuser
```

Run the dev server
```
python manage.py runserver
```

URL
```
http://localhost:8000/admin/
```
