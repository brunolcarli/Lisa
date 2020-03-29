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

    param : text : <str> or <list>
    algorythms : <list>
    return : <list>
    """
    skip = lambda same: same
    execute = {
        'sentece_segmentation': Resolver.resolve_sentence_segmentation,
        'tokenize': Resolver.resolve_tokenize,
        'stopwords': Resolver.resolve_remove_stopwords,
        'remove_puncts': Resolver.resolve_remove_puncts
    }
    for algorythm in algorythms:
        text = execute.get(algorythm, skip)(text)

    return text


def execute_reducer(text, reducer):
    """
    Aplica os extratores de lemma ou rdical

    param : text : <str> or <list>
    param : reducer : <str>
    return : <list>
    """
    skip = lambda same: same
    execute = {
        'stemmer': Resolver.resolve_stemming,
        'lemmer': Resolver.resolve_lemming
    }

    return execute.get(reducer, skip)(text)


def execute_processing(text, processor):
    """
    Aplica o processamento de análise de sentimentos através do classificador
    de texto.
    O retorno pode variar dependendo do algoritmo processador escolhido.

    param : text : <str> or <list>
    param : processor : <str>
    """
    skip = lambda same: same
    execute = {
        'lexical_text_classifier': Resolver.resolve_lexical_text_classifier,
        'dependencies': Resolver.resolve_dependency_parse,
        'word_offense': Resolver.resolve_word_offense
    }

    return execute.get(processor, skip)(text)
