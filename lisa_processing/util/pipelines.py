"""
Definição do processamento de pipelines
"""
from nltk import word_tokenize
from string import punctuation

from lisa_processing.util.nlp import (remove_puncts_from_string, sent_tokenize,
                                      remove_stopwords_from_str, word_tokenize)


class Normalizer:
    """
    Normaliza padrões de entrada e saída:
        <str> -> <list>
        <list> -> <str>
    """
    @staticmethod
    def list_to_string(token_list):
        """
        Recebe uma lista de strings e devolve uma string.

        param : token_list: <list>
        return : <str>
        """
        text = ''
        for token in token_list:
            if token not in punctuation:
                text += f'{token} '
            else:
                text = text.rstrip() + f'{token} '

        return text.rstrip()

    @staticmethod
    def string_to_list(text):
        """
        recebe uma string e devolve uma lista de tokens
        """
        return word_tokenize(text)


def execute_pre_processing(text, algorythms):
    """
    Passa uma entrada de texto por uma lista de algoritmos de pré-processamento.

    param : text : <str>
    algorythms : <list>
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
