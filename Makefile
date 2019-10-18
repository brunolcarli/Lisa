run:
	python manage.py runserver 0.0.0.0:8000 --settings=lisa.settings.development

migrate:
	python manage.py makemigrations --settings=lisa.settings.development
	python manage.py migrate --settings=lisa.settings.development
