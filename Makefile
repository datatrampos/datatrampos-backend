style:
	flake8 . ; isort . ; black .

flush:
	python manage.py flush --no-input

migrate:
	python manage.py migrate

create_superuser:
	python manage.py createsuperuser