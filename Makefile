run:
	python manage.py runserver 0.0.0.0:8000 --settings=lisa.settings.development

migrate:
	python manage.py makemigrations --settings=lisa.settings.development
	python manage.py migrate --settings=lisa.settings.development

install:
	pip install -r lisa/requirements/development.txt
	python -c "import nltk;nltk.download('punkt')"
	python -c "import nltk;nltk.download('stopwords')"
	python -c "import nltk;nltk.download('averaged_perceptron_tagger')"
	python -m spacy download pt
