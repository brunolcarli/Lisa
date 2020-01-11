"""
Módulo para funcionalidades relacionadas ao Processamento de Linguagem
Natural.
"""

import re
from random import choice
from string import punctuation
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from django.conf import settings


def get_word_polarity(word_input):
    """
    Retorna a polaridade de uma palavra

    param : word_input : <str>
    return : <int>
    """
    # Monta o dicionario de dados a paritr do córpus léxico
    data = {}
    # TODO: testar isso
    with open(settings.CORPORA_PATH['sentilex_lem'], 'r') as f:
        for row in f.readlines():
            splitter = row.find('.')
            word = (row[:splitter])
            word = stemming([word])[0]
            pol_loc = row.find('POL')
            polarity = (row[pol_loc+7:pol_loc+9]).replace(';','')
            data[word] = polarity

    # verifica se a palavra existe no corpus lexico
    if word_input.lower() in data.keys():
        return int(data[word_input.lower()])
    else:
        return 0


def text_classifier(text):
    """
    Classifica o sentimento do texto baseado 
    no método de Taboada et al. (2011)

    param text : <str>
    return : <float>
    """
    text_emotion = 0
    sentence_emotions = []

    negation_words = stemming([
        'jamais', 'nada', 'nem', 'nenhum', 'ninguém', 'nunca', 'não',
        'tampouco', 'insignigficância', 'insignificante', 'besteira',
        'argueiro', 'bobagem', 'futilidade', 'fútil'
    ])
    intensifiers = stemming([
            'mais', 'muito', 'demais', 'completamente', 'absolutamente',
            'totalmente', 'definitivamente', 'extremamente',
            'frequentemente', 'bastante', 'abundante', 'abundância',
            'enxurrada', 'exurbitância', 'fartura'
    ])
    reduction_words = stemming([
        'pouco', 'quase', 'menos', 'apenas', 'anormal', 'anômalo', 'banal',
        'atípico', 'excepcional', 'inabitual', 'raro', 'singular',
        'inusitado', 'unusual', 'incomum', 'insólito', 'aproximadamente',
        'triz'
    ])

    # Sentence segmentation
    sentences = sent_tokenize(text.lower())

    for sentence in sentences:

        # Cada sentença inicia neutra
        sentence_emotion = 0

        # Tokenization
        tokens = word_tokenize(sentence)

        # Sanitiza os tokens removendo os stop words
        tokenized = remove_stopwords(tokens)

        # Sanitiza removendo pontuações
        document = remove_punctuations(tokenized)

        document = stemming(document)

        # polariza a sentença
        for word in document:
            polarity = get_word_polarity(word)
            if any(w in intensifiers for w in document):
                if any(w in negation_words for w in document):
                    polarity /= 3
                else:
                    polarity *= 3

            elif any(w in reduction_words for w in document):
                if any(w in negation_words for w in document):
                    polarity *= 3
                else:
                    polarity /= 3

            else:
                # Adaptei: O original utiliza um -1 * polaridade
                polarity = 1 * polarity
    
            sentence_emotions.append((sentence_emotion + polarity))

    # A polaridade toral do texto é a média de emções nas sentenças
    text_emotion = sum(sentence_emotions) / len(sentence_emotions)

    return text_emotion * .1

def binary_wordmatch(input_text, word_list):
    """
    Percorre uma entrada de texto buscand identificar se uma palavra,
    composta de até duas palavras (Ex: Bom dia, Até breve, volte cedo)
    existe no contexto.

    A função recebe dois parâmetros: A entrada de texto e uma lista ou
    conjunto contendo as palávras que se pretende encontrar no texto.

    param : input_text : <str>
    param : word_list : <list>
    return : <bool>
    """
    #####################################################################
    # TODO: o spacy implementa bigramas, trigramas e ngramas, substituir
    # essa função por elas!
    #####################################################################

    prev_word = ''
    match = False
    for word in input_text.split():
        try:
            single_match = [re.fullmatch(word, target) for target in word_list]
        except:
            single_match = []

        try:
            binary_match =[re.fullmatch(f'{prev_word} {word}', target) for target in word_list]
        except:
            binary_match = []

        if any(single_match):
            match = True
            break
        elif any(binary_match):
            match = True
            break
        prev_word = word
    return match


def remove_stopwords(sentence):
    """
    Remove os stop words de uma sentença em português.

    param : sentence : <list> : Lista de tokens
    return: <list>
    """
    portuguese_stopwords = set(stopwords.words('portuguese'))
    return [word for word in sentence if word not in portuguese_stopwords]


def remove_punctuations(sentence):
    """
    Remove pontuações de uma sentença.

    param : sentence : <list> lista de tokens
    return : <list>
    """
    return [token for token in sentence if token not in punctuation]


def stemming(sentence):
    """
    Realiza o stemming nos tokens da sentença.

    param : sentecen : <list>
    return <list>
    """
    stemmer = SnowballStemmer('portuguese')
    return [stemmer.stem(token) for token in sentence]


def get_offense_level(text):
    """
    Mede o nível de baixo calão na frase dada a quantidade
    de "palavras feias" contidas no texto.
    """
    count = 0
    with open('corpora/hateset.txt', 'r') as f:
        data = set([i.lower()[:-1] for i in f.readlines()])

    for word in text:
        if word in data:
            count += 1

    try:
        average = count / len(text)
    except ZeroDivisionError:
        average = 0
    
    if average >= .25:
        response = True
    else:
        response = False

    return (response, average)


def basic_preprocess(text):
    """
    Realiza a atomização e remove as pontuações de um texto.

    param : text : <str>
    return : <list>
    """
    sentences = sent_tokenize(text)
    pre_processed_tokens = []
    for sentence in sentences:
        tokenized = word_tokenize(sentence)
        raw_tokens = remove_punctuations(tokenized)
        clean_tokens = remove_stopwords(raw_tokens)
        for token in clean_tokens:
            pre_processed_tokens.append(token)

    return pre_processed_tokens
