import os
import spacy
from lisa_processing.util.nlp import stemming
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa.settings.development")
django.setup()

from lisa_processing.models import Term
nlp = spacy.load('pt')


def populate_terms():
    """
    Inicializa a tabela de termos com dados da corpora.
    """
    print('populating from sentilex...')
    with open('corpora/lexical_data/SentiLex-lem-PT02.txt', 'r') as f:
        sentilex = [i.strip().lower() for i in f.readlines()]

    # suite.PoS=Adj;TG=HUM:N0;POL:N0=-1;ANOT=MAN
    for row in sentilex:
        data = {}
        text, meta_data = row.split('.')
        pos, _, pol, *_ = meta_data.split(';')
        _, pos = pos.split('=')
        _, pol = pol.split('=')

        data['text'] = text
        data['part_of_speech'] = pos
        data['polarity'] = pol

        try:
            term = Term.objects.create(**data)
        except Exception as _:
            continue

        term.save()

    print(f'Created {Term.objects.all().count()} objects.')


def populate_from_hateset():
    """
    Inicializa a tabela de termos com dados da corpora de exemplos ofensivos.
    """
    print('populating from hateset...')
    with open('corpora/lexical_data/hateset.txt', 'r') as f:
        hateset = [i.strip().lower() for i in f.readlines()]

    for sample in hateset:

        term, _ = Term.objects.get_or_create(text=sample)

        term.is_offensive = True
        term.save()

    print('DB update from hateset')


def update_terms_metadata():
    """
    Atualiza os metadados dos termos do banco de dados
    """
    terms = Term.objects.all()

    for term in terms:
        tokens = nlp(term.text)

        term.part_of_speech = tokens[0].pos_
        term.is_currency = tokens[0].is_currency
        term.is_punct = tokens[0].is_punct
        term.is_stop = tokens[0].is_stop
        term.is_digit = tokens[0].is_digit

        term.lemma = tokens[0].lemma
        term.root = stemming([term.text])
        term.save()

    print('Updated terms metadata.')
