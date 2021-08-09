import os
import spacy
from lisa_processing.util.nlp import stemming
from lisa_processing.models import Term
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lisa.settings.development")
django.setup()
nlp = spacy.load('pt')


def populate_terms():
    """
    Inicializa a tabela de termos com dados da corpora.
    """
    print('populating from sentilex...')
    with open('corpora/lexical_data/SentiLex-lem-PT02.txt', 'r') as f:
        sentilex = [i.strip().lower() for i in f.readlines()]

    with open('corpora/lexical_data/hateset.txt', 'r') as f:
        hateset = set([i.strip().lower() for i in f.readlines()])

    # suite.PoS=Adj;TG=HUM:N0;POL:N0=-1;ANOT=MAN
    for row in sentilex:
        data = {}
        term, meta_data = row.split('.')
        pos, _, pol, *_ = meta_data.split(';')
        _, pos = pos.split('=')
        _, pol = pol.split('=')

        data['text'] = term
        data['part_of_speech'] = pos
        data['polarity'] = pol

        if term in hateset:
            data['is_offensive'] = True

        tokens = nlp(term)

        data['is_currency'] = tokens[0].is_currency
        data['is_punct'] = tokens[0].is_punct
        data['is_stop'] = tokens[0].is_stop
        data['is_digit'] = tokens[0].is_digit

        data['lemma'] = tokens[0].lemma
        data['root'] = stemming([term])

        try:
            Term.objects.create(**data)
        except Exception as _:
            continue

    print(f'Created {Term.objects.all().count()} objects.')


def populate_from_hateset():
    """
    Inicializa a tabela de termos com dados da corpora de exemplos ofensivos.
    """
    print('populating from hateset...')
    with open('corpora/lexical_data/hateset.txt', 'r') as f:
        hateset = [i.strip().lower() for i in f.readlines()]

    counter = 0
    for sample in hateset:
        data = {}
        data['text'] = sample
        data['is_offensive'] = True

        tokens = nlp(sample)

        data['part_of_speech'] = tokens[0].pos_
        data['polarity'] = sum([i.sentiment for i in tokens]) / len(tokens)
        data['is_currency'] = all([i.is_currency for i in tokens])
        data['is_punct'] = all([i.is_punct for i in tokens])
        data['is_stop'] = all([i.is_stop for i in tokens])
        data['is_digit'] = all([i.is_digit for i in tokens])

        data['lemma'] = (' '.join([i.lemma_ for i in tokens])).strip()
        data['root'] = stemming([sample])

        try:
            Term.objects.create(**data)
        except Exception as _:
            continue

        counter += 1

    print(f'Created {Term.objects.all().count()} objects.')
