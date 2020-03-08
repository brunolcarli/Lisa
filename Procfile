web: python -c "import nltk;nltk.download('punkt')"
web: python -c "import nltk;nltk.download('stopwords')"
web: python -c "import nltk;nltk.download('averaged_perceptron_tagger')"
web: python -m spacy download pt
web: python manage.py migrate
web: gunicorn lisa.wsgi --log-file -