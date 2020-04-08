"""
Definição do processamento de pipelines
"""
from lisa_processing.util.nlp import (remove_puncts_from_string, sent_tokenize,
                                      remove_stopwords_from_str, word_tokenize)
from lisa_processing.resolvers import Resolver
from lisa_processing.util.normalizer import Normalizer


class CustomPipeline:
    """
    Possui métodos de execução de componentes de um pipeline customizavel.
    """
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def execute_data_extraction(input_data, feature):
        """
        Aplica o processamento de extração de dados e análise sintática à uma
        entrada.
        O retorno pode variar dependendo da feature fornecida.

        param : input_data : <str> ou <list>
        param : feature <str>
        """
        skip = lambda same: same
        execute = {
            'dependencies': Resolver.resolve_dependency_parse,
            'entities': Resolver.resolve_named_entity,
            'pos': Resolver.resolve_part_of_speech,
            'lexical_text_classifier': Resolver.resolve_lexical_text_classifier,
            'word_offense': Resolver.resolve_word_offense,
            'text_offense': Resolver.resolve_text_offense,
            'word_pol': Resolver.resolve_word_polarity,
        }

        return execute.get(feature, skip)(input_data)
