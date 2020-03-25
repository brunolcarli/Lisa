"""
Definição do processamento de pipelines
"""
from lisa_processing.util.nlp import (remove_puncts_from_string, sent_tokenize,
                                      remove_stopwords_from_str, word_tokenize)
from lisa_processing.resolvers import Resolver
from lisa_processing.util.normalizer import Normalizer


def execute_pre_processing(text, algorythms):
    """
    Passa uma entrada de texto por uma lista de algoritmos de pré-processamento.

    param : text : <str>
    algorythms : <list>
    return : <str>
    """
    refresh = Normalizer()
    skip = lambda text: refresh.string_to_list(text)
    execute = {
        'sentece_segmentation': sent_tokenize,
        'tokenize': word_tokenize,
        'stopwords': remove_stopwords_from_str,
        'remove_puncts': remove_puncts_from_string
    }
    for algorythm in algorythms:
        text = execute.get(algorythm, skip)(text)
        text = refresh.list_to_string(text)

    return text


def execute_reducer(text, reducer):
    """
    Aplica os extratores de lemma ou rdical

    param : text : <str>
    param : reducer : <str>
    return : <str>
    """
    refresh = Normalizer()
    skip = lambda text: refresh.string_to_list(text)
    execute = {
        'stemmer': Resolver.resolve_stemming,
        'lemmer': Resolver.resolve_lemming
    }
    output = execute.get(reducer, skip)(text)
    return refresh.list_to_string(output)
