"""
Definição do processamento de pipelines
"""
from nltk import word_tokenize
from string import punctuation


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
