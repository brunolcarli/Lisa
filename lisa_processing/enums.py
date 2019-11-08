from graphene import Enum, InputObjectType

class Algorithms(Enum):
    """
    Define enumeradores para a escolha dos algoritmos a serem
    utilizados para o processamento das requisições.
    """
    SPACY = 'spacy'
    NLTK = 'nltk'
