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
    stemmed_word = stemming([word_input])[0]
    if stemmed_word.lower() in data.keys():
        return int(data[stemmed_word.lower()])
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

    # A polaridade total do texto é a média de emoções nas sentenças
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
            binary_match = [re.fullmatch(f'{prev_word} {word}', target) for target in word_list]
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


def get_hateset():
    """
    Abre o corpus hateset.txt cujo possui amostras de termos ofensivos,
    realiza o slicing das linhas do arquivo retornando somente o termo principal
    para o stemmer, filtrando as duplicatas e retornando um conjunto (set)
    contendo a raiz dos termos do corpus.

    return : <set> |> <str> : Conjunto de termos stemizados.
    """
    with open(settings.CORPORA_PATH['hateset']) as f:
        data = set(stemming([i.lower()[:-1] for i in f.readlines()]))

    return data


def get_offense_level(text):
    """
    Mede o nível de baixo calão na frase dada a quantidade
    de "palavras feias" contidas no texto.
    """
    count = 0

    # pré-processa a entrada e retorna as amostras também pré-processadas
    text = stemming(basic_preprocess(text))
    data = get_hateset()

    # Contabiliza as ocorrências
    for word in text:
        if word in data:
            count += 1

    # Se a entrada conter somente stopwords, possivelmente o pre-processamento
    # irá "esvaziar" a entrada, resultando em uma possível divisão por zero
    try:
        average = count / len(text)
    except ZeroDivisionError:
        average = 0

    # Define como sugestão de ofensa se a média for maior ou igual a 25%
    response = average >= .25 or False

    return (response, average)


def get_word_offense_level(word_list):
    """
    Verifica se as palavras fornecidas são ofensivas baseadas no hateset.
    Retorna uma lista de tuplas contendo:
        - Palavra analisada;
        - Inteiro representando se ofensivo (1) ou não ofensivo (0);
        - Formato [(<str>, <int>), (<str>, <int>), ...]
    param : word_list : <list> |> <str> : Lista de palavras;
    return : <list> |> <tuple>
    """
    result = []

    # stemiza a entrada e recupera as amostras também pré-processadas
    tokens = stemming(remove_stopwords(remove_punctuations(word_list)))
    data = get_hateset()

    # TODO: Pensar em uma forma de retornar na tupla o termo completo e não a raio
    for token in tokens:
        if token in data:
            result.append((token, 1))
        else:
            result.append((token, 0))
    return result


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
