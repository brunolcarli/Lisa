# Local commands
run:
	python manage.py runserver 0.0.0.0:2154 --settings=lisa.settings.development

migrate:
	python manage.py makemigrations --settings=lisa.settings.development
	python manage.py migrate --settings=lisa.settings.development

install:
	pip install -r lisa/requirements/development.txt
	python -c "import nltk;nltk.download('punkt')"
	python -c "import nltk;nltk.download('stopwords')"
	python -c "import nltk;nltk.download('averaged_perceptron_tagger')"
	python -m spacy download pt


# Repl.it Commands
run_replit:
	python3 manage.py runserver 0.0.0.0:3000 --settings=lisa.settings.replit

migrate_replit:
	python3 manage.py makemigrations --settings=lisa.settings.replit
	python3 manage.py migrate --settings=lisa.settings.replit

install_replit:
	pip3 install -r lisa/requirements/development.txt
	python3 -c "import nltk;nltk.download('punkt')"
	python3 -c "import nltk;nltk.download('stopwords')"
	python3 -c "import nltk;nltk.download('averaged_perceptron_tagger')"
	python3 -m spacy download pt

replit_pipeline:
	make install_replit
	make migrate_replit
	make run_replit


# Docker
container:
	docker-compose build
	docker-compose up


populate_terms:
	python -c "from lisa_processing.util.populate import populate_terms; populate_terms()"

populate_hateset:
	python -c "from lisa_processing.util.populate import populate_from_hateset; populate_from_hateset()"


populate:
	make populate_terms
	make populate_hateset
