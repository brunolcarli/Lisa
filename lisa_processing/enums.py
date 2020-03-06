from graphene import Enum, InputObjectType

class Algorithms(Enum):
    """
    Define enumeradores para a escolha dos algoritmos a serem
    utilizados para o processamento das requisições.
    """
    SPACY = 'spacy'
    NLTK = 'nltk'

class WordPolarityAlgorithms(Enum):
    """
    Algoritmos para processar polaridade de palavras
    """
    SPACY = 'spacy'
    LEXICAL = 'lexical'
