r"""
   ___ __ _     _  _ ___    __ __    __    _ 
|   | (_ |_|   |_||_) |    (_ /  |_||_ |V||_|
|___|___)| |   | ||  _|_   __)\__| ||__| || |

contact info: brunolcarli@gmail.com
"""
import sys
import spacy
import graphene
from django.conf import settings
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
from lisa_processing.enums import Algorithms, WordPolarityAlgorithms
from lisa_processing.util.nlp import get_word_polarity, text_classifier


class DependencyParseType(graphene.ObjectType):
    """
    Padrão de resposta para processamentos de parsing de dependência.
    """
    element = graphene.String()
    children = graphene.List(graphene.String)
    ancestors = graphene.List(graphene.String)


class NamedEntityType(graphene.ObjectType):
    """
    Padrão de resposta para processamento de entidades nomeadas.
    """
    term = graphene.String()
    entity = graphene.String()


class WordPolarityType(graphene.ObjectType):
    """
    Padrão de resposta para processamentos de identificação de polaridades
    de palávras.
    """
    word = graphene.String()
    polarity = graphene.Float()


class Query(graphene.ObjectType):
    """
    Queries da lisa:
        Disponibiliza as consultas de processamento de linguagem natural e
        análise de sentimentos da API.
    """

    ##########################################################################
    # SENTENCE SEGMENTATION
    ##########################################################################
    sentence_segmentation = graphene.List(
        graphene.String,
        text=graphene.String(
            description='Input text for sentece segmentation!',
            required=True
        ),
        description='Process a sentence segmentation over a text input.'
    )
    def resolve_sentence_segmentation(self, info, **kwargs):
        """
        Processa a requisição de sentence segmentation conforme RF001.
        """
        text = kwargs.get('text')
        segmented_text = sent_tokenize(text)

        return segmented_text

    ##########################################################################
    # WORD TOKENIZE
    ##########################################################################
    word_tokenize = graphene.List(
        graphene.String,
        text=graphene.String(
            required=True,
            description='Text input for word tokenizing.'
        ),
        description='Process the word tokenizer request.'
    )
    def resolve_word_tokenize(self, info, **kwargs):
        """
        Processa requisição para atomização
        """
        text = kwargs.get('text')
        tokenized = word_tokenize(text)

        return tokenized

    ##########################################################################
    # PART OF SPEECH
    ##########################################################################
    part_of_speech = graphene.List(
        graphene.List(
            graphene.String
        ),
        non_tokenized_text=graphene.String(
            description='Process part of speech with a non tokenized input.'
        ),
        tokenized_text=graphene.List(
            graphene.String,
            description='Process part of speech with a tokenized input.'
        ),
        description='Process request for part of speech.'
    )
    def resolve_part_of_speech(self, info, **kwargs):
        """
        Processa requisição de part of speech
        """

        # não pode não passar nenhum filtro
        if not kwargs:
            raise Exception('Please choose a filter input option!')

        # captura os possíveis filtros
        tokenized = kwargs.get('tokenized_text')
        non_tokenized = kwargs.get('non_tokenized_text')

        # não pode passar os dois filtros ao mesmo tempo
        if tokenized and non_tokenized:
            raise Exception('Please, input only one filter!')

        elif tokenized:
            return pos_tag(tokenized)

        else:
            return pos_tag(word_tokenize(non_tokenized))

    ##########################################################################
    # LEMMING
    ##########################################################################
    lemmatize = graphene.List(
        graphene.String,
        text=graphene.String(
            description='Process lemmatization with a non tokenized text input.'
        ),
        description='Lemmatize an inputed text or list of words.'
    )
    def resolve_lemmatize(self, info, **kwargs):
        """
        Retorna o processamento de lematização de uma entrada de texto ou
        lista de palavras.
        """

        # Não pode não fornecer nenhum filtro
        if not kwargs:
            raise Exception('Please choose a filter input option!')

        # captura os possíveis filtros
        text = kwargs.get('text')

        # Tenta carregar pt por padrao, se nao der carrega o pt_core_news
        try:
            SPACY = spacy.load('pt')
        except OSError:
            sys.stdout.write('Failed loading spcy pt, trying to load core_news...\n')
            SPACY = spacy.load('pt_core_news_sm')
        else:
            raise Exception('Failed loading SpaCy!')
        tokens = SPACY(text)
        data = [token for token in tokens]

        return [token.lemma_ for token in data]

    ##########################################################################
    # STOP WORDS
    ##########################################################################
    remove_stop_words = graphene.List(
        graphene.String,
        text=graphene.String(
            required=True,
            description='Input text for process the stop words removal.'
        ),
        algorithm=graphene.Argument(
            Algorithms,
            description='Defines an processing algorithm. Default NLTK'
        ),
        description='Remove stop words from inputed text.'
    )

    def resolve_remove_stop_words(self, info, **kwargs):
        """
        Remove as palavras vazias do texto inserido e retorna uma lista das
        palávras restantes no texto.
        """
        algorithm = kwargs.get('algorithm', 'nltk')
        text_input = kwargs.get('text')
        portuguese_stopwords = stopwords.words('portuguese')

        if algorithm == 'nltk':
            tokens = word_tokenize(text_input)
            return [word for word in tokens if word not in portuguese_stopwords]

        # Tenta carregar pt por padrao, se nao der carrega o pt_core_news
        try:
            SPACY = spacy.load('pt')
        except OSError:
            sys.stdout.write('Failed loading spcy pt, trying to load core_news...\n')
            SPACY = spacy.load('pt_core_news_sm')
        else:
            raise Exception('Failed loading SpaCy!')
        doc = SPACY(text_input)
        return [word for word in doc if not word.is_stop]

    ##########################################################################
    # DEPENDENCY PARSING
    ##########################################################################
    dependency_parse = graphene.List(
        DependencyParseType,
        text=graphene.String(
            description='Input text for dependency parsing processing.',
            required=True
        ),
    )

    def resolve_dependency_parse(self, info, **kwargs):
        """
        Processa o parsing de dependências e retorna uma lista contendo
        as palávras da sentença, seus dependentes e antecessores.
        """
        text = kwargs.get('text')
        # Tenta carregar pt por padrao, se nao der carrega o pt_core_news
        try:
            SPACY = spacy.load('pt')
        except OSError:
            sys.stdout.write('Failed loading spcy pt, trying to load core_news...\n')
            SPACY = spacy.load('pt_core_news_sm')
        else:
            raise Exception('Failed loading SpaCy!')
        doc = SPACY(text)
        result = []

        for word in doc:
            result.append({
                'element': word,
                'children': list(word.children),
                'ancestors': list(word.ancestors)
            })

        return result

    ##########################################################################
    # NAMED ENTITY
    ##########################################################################
    named_entity = graphene.List(
        NamedEntityType,
        text=graphene.String(
            description='Input text for named entity processing.',
            required=True
        ),
    )

    def resolve_named_entity(self, info, **kwargs):
        """
        Processa a resolução de entidades nomeadas a partir de um texto.
        """
        text_input = kwargs.get('text')
        # Tenta carregar pt por padrao, se nao der carrega o pt_core_news
        try:
            SPACY = spacy.load('pt')
        except OSError:
            sys.stdout.write('Failed loading spcy pt, trying to load core_news...\n')
            SPACY = spacy.load('pt_core_news_sm')
        else:
            raise Exception('Failed loading SpaCy!')
        doc = SPACY(text_input)
        return [NamedEntityType(*(i, i.label_)) for i in doc.ents]

    ##########################################################################
    # Word Polarity
    ##########################################################################
    word_polarity = graphene.List(
        WordPolarityType,
        word_list=graphene.List(
            graphene.String,
            description='List of words to process',
            required=True
        ),
        algorithm=graphene.Argument(
            WordPolarityAlgorithms,
            description='Algorythm to process the the text. Default=LEXICAL'
        )
    )
    def resolve_word_polarity(self, info, **kwargs):
        """
        Processa a resolução de polaridades de palavras.
        O Processamento aceita uma lista de palávras, retornando desta forma,
        uma lista de objetos contendo a palávra processada e sua polaridade.
        """
        word_list = kwargs.get('word_list')
        algorithm = kwargs.get('algorithm', 'lexical')

        if algorithm == 'spacy':
            # Tenta carregar pt por padrao, se nao der carrega o pt_core_news
            try:
                SPACY = spacy.load('pt')
            except OSError:
                sys.stdout.write('Failed loading spcy pt, trying to load core_news...\n')
                SPACY = spacy.load('pt_core_news_sm')
            else:
                raise Exception('Failed loading SpaCy!')    
            doc = [SPACY(word) for word in word_list]
            return [WordPolarityType(word=w.text, polarity=w.sentiment) for w in doc]

        return [WordPolarityType(word=w, polarity=get_word_polarity(w)) for w in word_list]

    ##########################################################################
    # text classifier
    ##########################################################################
    text_classifier = graphene.Float(
        text=graphene.String(required=True, description='Text to classify.'),
        algorithm=graphene.Argument(
            WordPolarityAlgorithms,
            description='Defines the processing algorithm backend. Default=LEXICAL'
        )
    )
    def resolve_text_classifier(self, info, **kwargs):
        """
        Classifica a polaridade do texto de acordo com o algoritmo léxico de
        Taboada, retornado do processamento um númerod e ponto flutuante entre
        -1 e 1 podendo representar a negatividade, neutralidade ou positividade
        do texto processado.
        """
        text = kwargs.get('text')
        algorithm = kwargs.get('algorithm', 'lexical')

        if algorithm == 'spacy':
            # Tenta carregar pt por padrao, se nao der carrega o pt_core_news
            try:
                SPACY = spacy.load('pt')
            except OSError:
                sys.stdout.write('Failed loading spcy pt, trying to load core_news...\n')
                SPACY = spacy.load('pt_core_news_sm')
            else:
                raise Exception('Failed loading SpaCy!')    
            doc = SPACY(text)
            return doc.sentiment

        return text_classifier(text)

    ##########################################################################
    # OVO DE PÁSCOA
    ##########################################################################
    lisa = graphene.List(graphene.String)
    def resolve_lisa(self, info, **kwargs):
        """
        Isso é um ovo de páscoa.
        """
        lisa_ascii = [
            r'''|          _     _            |''',
            r'''|        ,':`._.':`.          |''',
            r'''|    ..-':::::::'   `--..     |''',
            r'''|   \:::::::::          /    |''',
            r'''|   _`.::::::          `._    |''',
            r'''| .':::_.`--'.  ,'--'._   `,  |''',
            r'''|  `.:::  o   ::  o   :  ,'   |''',
            r'''|   ,':`.____.;:.____.' `.    |''',
            r'''-------------------------------''',
            f'Version: {settings.VERSION}'
        ]
        return lisa_ascii
