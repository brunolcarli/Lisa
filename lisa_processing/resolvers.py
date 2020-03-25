"""
Resolução dos algoritmos chamados nas queries.
"""
import spacy
from lisa_processing.util.nlp import stemming
from lisa_processing.util.normalizer import Normalizer

SPACY = spacy.load('pt')

class Resolver:
    @staticmethod
    def resolve_lemming(text):
        """
        Resolução do processamento de lemming.

        param : text : <str>
        return : <list>
        """
        tokens = SPACY(text)

        return [token.lemma_ for token in tokens]

    @staticmethod
    def resolve_stemming(text):
        """
        Resolução do processamento de stemming

        param : text : <str>
        return : <list>
        """
        normalizer = Normalizer()
        tokens = normalizer.string_to_list(text)
        return stemming(tokens)
