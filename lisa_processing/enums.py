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


class Processing(Enum):
    """
    Constantes representando os algoritmos de processamento.
    """
    LEXICAL_TEXT_CLASSIFIER = 'lexical_text_classifier'
    WORD_OFFENSE = 'word_offense'
    TEXT_OFFENSE = 'text_offense'
    WORD_POLARITY = 'word_pol'
    NAMED_ENTITY = 'entities'
    DEPENDECY_PARSE = 'dependencies'
    PART_OF_SPEECH = 'pos'


class Reducers(Enum):
    """
    Constantes representando os processadores de extração de lemmas e radicais.
    """
    STEMMING = 'stemmer'
    LEMMING = 'lemmer'
