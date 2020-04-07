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


class Language(Enum):
    """
    Define constantes para a linguagem utilizanda em determinados textos.
    """
    # Por enquanto Pt-Br e English (US)
    PTBR = 'pt-br'
    ENGLISH = 'en'


class PreProcess(Enum):
    """
    Constantes representando os algoritmos de pre-processamento.
    """
    SENTENCE_SEGMENTATION = 'sentece_segmentation'
    TOKENIZE = 'tokenize'
    REMOVE_STOPWORDS = 'stopwords'
    REMOVE_PUNCTUATION = 'remove_puncts'


class DataExtraction(Enum):
    """
    Constantes representando os algoritmos de extração de dados e análise
    sintática.
    """
    NAMED_ENTITY = 'entities'
    DEPENDECY_PARSE = 'dependencies'
    PART_OF_SPEECH = 'pos'
    LEXICAL_TEXT_SENTIMENT = 'lexical_text_classifier'
    WORD_OFFENSE = 'word_offense'
    TEXT_OFFENSE = 'text_offense'
    WORD_POLARITY = 'word_pol'


class Reducers(Enum):
    """
    Constantes representando os processadores de extração de lemmas e radicais.
    """
    STEMMING = 'stemmer'
    LEMMING = 'lemmer'
