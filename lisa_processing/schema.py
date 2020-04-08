r"""
   ___ __ _     _  _ ___    __ __    __    _ 
|   | (_ |_|   |_||_) |    (_ /  |_||_ |V||_|
|___|___)| |   | ||  _|_   __)\__| ||__| || |

contact info: brunolcarli@gmail.com
"""
import spacy
import graphene
from django.conf import settings
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from lisa_processing import enums
from lisa_processing.resolvers import Resolver
from lisa_processing.util.types import DynamicScalar
from lisa_processing.util.pipelines import CustomPipeline
from lisa_processing.util.nlp import stemming as stem
from lisa_processing.util.nlp import (get_word_polarity, text_classifier,
                                      get_offense_level, get_word_offense_level,
                                      is_stopword)
from lisa_processing.util.tools import (get_pos_tag_description,
                                       get_entity_description)


SPACY = spacy.load('pt')

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
    description = graphene.String()


class WordPolarityType(graphene.ObjectType):
    """
    Padrão de resposta para processamentos de identificação de polaridades
    de palávras.
    """
    word = graphene.String()
    polarity = graphene.Float()


class TextOffenseType(graphene.ObjectType):
    """
    Padrão de resposta para requisições de TextOffense.
    """
    text = graphene.String(description='Processed text!')
    average = graphene.Float(
        description='Avarage calc on based on bad words counting!'
    )
    result = graphene.Boolean(
        description='True if the sentence is offensive, False if not!'
    )


class WordOffenseType(graphene.ObjectType):
    """
    Padrão de objeto contido na lista retornada como resposta na requisição de
    processamento de wordOffenseLevel (Nível Ofensivo de palavras)
    """
    root = graphene.String(description='Stemmed root from the inputed term')
    value = graphene.Int(
        description='Integer that indicates if the term may be offensive! 1 for yes 0 for no.'
    )
    is_offensive = graphene.Boolean(
        description='Suggests if the term is offensive'
    )


class StemmingType(graphene.ObjectType):
    """
    Define a estrutura de resposta da requisição de stemming
    """
    token = graphene.String(description='Original given token.')
    root = graphene.String(
        description='Stemmed root extracted from the original term.'
    )


class PartOfSpeechType(graphene.ObjectType):
    """
    Define a estrutura de resposta da requisição de partOfSpeech
    """
    token = graphene.String(description='Analyzed token.')
    tag = graphene.String(description='Identified tag.')
    description = graphene.String(description='Explicit tag meaning.')

    # def resolve_description(self, info, **kwargs):
    #     self.description = get_pos_tag_description(self.tag)


class InspectTokenType(graphene.ObjectType):
    """
    Define a estrutura da resposta a inspectTokens, apresentandos
    dados de cada token fornecido.
    """
    token = graphene.String(description='Analyzed token.')
    is_alpha = graphene.Boolean(description='Indicates if token is alpha numeric.')
    is_ascii = graphene.Boolean(description='Indicates if token is ascii.')
    is_currency = graphene.Boolean(description='Indicates if token is a currency value')
    is_digit = graphene.Boolean(description='Indicates if token is a digit')
    is_punct = graphene.Boolean(description='Indicates if token is punctuation')
    is_space = graphene.Boolean(description='Indicates if token is whitespace')
    is_stop = graphene.Boolean(description='Indicates if token is a stop word')
    lemma = graphene.String(description='The token lemma representation')
    pos_tag = graphene.String(description='The token part of speech tag representation')
    vector = graphene.List(
        graphene.Float,
        description='Vector data of the token'
    )
    polarity = graphene.Int(description='The token extracted polarity')
    is_offensive = graphene.Boolean(description='Token is a offensive term.')
    root = graphene.String(description='Stemmed root extracted from token.')


class CustomPipelineType(graphene.ObjectType):
    """
    Define a estrutura de resposta para consultas de pipeline customizado
    """
    text = graphene.String(description='Processed text.')
    chosen_pre_processment = graphene.List(
        enums.PreProcess,
        description='List of the selected preprocessing features.'
    )
    chosen_reducer = enums.Reducers(
        description='Selected word reducer feature.'
    )
    chosen_data_extraction = enums.DataExtraction(
        description='Selected data extraction feature.'
    )
    output = DynamicScalar(description='Pipeline output.')
    token_inspection = graphene.List(
        InspectTokenType,
        description='Enables the return of inspected tokens of the pre-processed'\
                    ' data at cost of longer processing time. Default=False'
    )


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
        return Resolver.resolve_sentence_segmentation(kwargs.get('text'))

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
        return Resolver.resolve_tokenize(kwargs.get('text'))

    ##########################################################################
    # PART OF SPEECH
    ##########################################################################
    part_of_speech = graphene.List(
        PartOfSpeechType,
        text=graphene.String(
            required=True,
            description='Process part of speech with a non tokenized input.'
        ),
        description='Process request for part of speech.'
    )

    def resolve_part_of_speech(self, info, **kwargs):
        """
        Processa requisição de part of speech
        """
        resolved_data = Resolver.resolve_part_of_speech(kwargs.get('text'))
        return [PartOfSpeechType(**data) for data in resolved_data]

    ##########################################################################
    # LEMMING
    ##########################################################################
    lemmatize = graphene.List(
        graphene.String,
        text=graphene.String(
            required=True,
            description='Process lemmatization with a non tokenized text input.'
        ),
        description='Lemmatize an inputed text or list of words.'
    )

    def resolve_lemmatize(self, info, **kwargs):
        """
        Retorna o processamento de lematização de uma entrada de texto ou
        lista de palavras.
        """
        return Resolver.resolve_lemming(kwargs.get('text'))

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
            enums.Algorithms,
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
        return Resolver.resolve_dependency_parse(kwargs.get('text'))

    ##########################################################################
    # NAMED ENTITY
    ##########################################################################
    named_entity = graphene.List(
        NamedEntityType,
        text=graphene.String(
            description='Input text for named entity processing.',
            required=True
        ),
        description='Extracts the entities from text.'
    )

    def resolve_named_entity(self, info, **kwargs):
        """
        Processa a resolução de entidades nomeadas a partir de um texto.
        """
        text_input = kwargs.get('text')
        doc = SPACY(text_input)

        return [
            NamedEntityType(
                term=ent.text,
                entity=ent.label_,
                description=get_entity_description(ent.label_)
            ) for ent in doc.ents
        ]

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
            enums.WordPolarityAlgorithms,
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
            doc = [SPACY(word) for word in word_list]
            return [WordPolarityType(word=w.text, polarity=w.sentiment) for w in doc]

        return [WordPolarityType(word=w, polarity=get_word_polarity(w)) for w in word_list]

    ##########################################################################
    # text classifier
    ##########################################################################
    sentiment_extraction = graphene.Float(
        text=graphene.String(required=True, description='Text to classify.'),
        algorithm=graphene.Argument(
            enums.WordPolarityAlgorithms,
            description='Defines the processing algorithm backend. Default=LEXICAL'
        )
    )

    def resolve_sentiment_extraction(self, info, **kwargs):
        """
        Extrai o sentimento com o algoritmo léxico de Taboada, retornado do
        processamento um número de ponto flutuante entre -1 e 1 podendo
        representar a negatividade, neutralidade ou positividade
        do texto processado.
        """
        text = kwargs.get('text')
        algorithm = kwargs.get('algorithm', 'lexical')

        if algorithm == 'spacy':
            doc = SPACY(text)
            return doc.sentiment

        return text_classifier(text)

    ##########################################################################
    # Text Offense
    ##########################################################################
    text_offense_level = graphene.Field(
        TextOffenseType,
        text=graphene.String(
            required=True,
            description='Text string to be classified!'
        ),
        description='Classifies the text based on bad words included'
    )

    def resolve_text_offense_level(self, info, **kwargs):
        text = kwargs.get('text')
        result, average = get_offense_level(text)
        return TextOffenseType(text=text, average=average, result=result)

    ##########################################################################
    # Word Offense
    ##########################################################################
    word_offense_level = graphene.List(
        WordOffenseType,
        word_list=graphene.List(
            graphene.String,
            required=True,
            description='List of words to be classified!',
        ),
        description='Classifies the terms as offensive or not offensive.'
    )

    def resolve_word_offense_level(self, info, **kwargs):
        words = kwargs.get('word_list')
        data = get_word_offense_level(words)

        response = []
        for result in data:
            response.append(
                WordOffenseType(
                    root=result[0],
                    value=result[1],
                    is_offensive=bool(result[1])
                )
            )

        return response

    ##########################################################################
    # stemming
    ##########################################################################
    stemming = graphene.List(
        StemmingType,
        text=graphene.String(
            required=True,
            description='Text to be stemmed!'
        ),
        description='Returns root of each listed word'
    )

    def resolve_stemming(self, info, **kwargs):
        data = Resolver.resolve_stemming(kwargs.get('text'))

        paired_data = list(zip(kwargs.get('text').split(), data))
        return [StemmingType(token=pair[0], root=pair[1]) for pair in paired_data]

    ##########################################################################
    # InspectTokens
    ##########################################################################
    inspect_tokens = graphene.List(
        InspectTokenType,
        text=graphene.String(
            required=True,
            description='Message to be parsed and inspected.',
        ),
        description='Returns full data of each token on the sentence.'
    )

    def resolve_inspect_tokens(self, info, **kwargs):
        response = []
        tokens = SPACY(kwargs.get('text'))

        for token in tokens:
            response.append(
                InspectTokenType(
                    token=token.text,
                    is_alpha=token.is_alpha,
                    is_ascii=token.is_ascii,
                    is_currency=token.is_currency,
                    is_digit=token.is_digit,
                    is_punct=token.is_punct,
                    is_space=token.is_space,
                    is_stop=is_stopword(token.text),
                    lemma=token.lemma_,
                    pos_tag=get_pos_tag_description(token.pos_),
                    vector=token.vector,
                    polarity=get_word_polarity(token.text),
                    is_offensive=get_offense_level(token.text)[0],
                    root=stem([token.text])[0]
                )
            )

        return response

    ##########################################################################
    # Similarity
    ##########################################################################
    similarity = graphene.Float(
        first_token=graphene.String(
            required=True,
            description='First term.'
        ),
        second_token=graphene.String(
            required=True,
            description='Second term.'
        ),
        description='Compares the similarity between first and second token.'
    )

    def resolve_similarity(self, info, **kwargs):
        first = SPACY(kwargs.get('first_token'))
        second = SPACY(kwargs.get('second_token'))

        return first.similarity(second)

    ##########################################################################
    # Custom pipeline
    ##########################################################################
    custom_pipeline = graphene.Field(
        CustomPipelineType,
        text=graphene.String(
            required=True,
            description='Text input to be processed!'
        ),
        pre_process=graphene.List(
            enums.PreProcess,
            description='Pre-process oeprations in the given ordering'
        ),
        reducer=graphene.Argument(
            enums.Reducers,
            description='Root and lemma reducers.'
        ),
        data_extraction=graphene.Argument(
            enums.DataExtraction,
            description='Process data extraction operations over the data.'
        ),
        enable_token_inspection=graphene.Boolean(
            description='Enables the token inspection before final processing.'
        ),
        description='Returns the result of a custom pipeline!'
    )

    def resolve_custom_pipeline(self, info, **kwargs):
        text = kwargs.get('text')
        output = text

        pre_processing = kwargs.get('pre_process')
        reducer = kwargs.get('reducer')
        data_extraction = kwargs.get('data_extraction')

        if pre_processing:
            output = CustomPipeline.execute_pre_processing(output, pre_processing)

        if reducer:
            output = CustomPipeline.execute_reducer(output, reducer)

        # Inspeciona os tokens antes do processamento final
        if kwargs.get('enable_token_inspection', False):
            token_inspection = [InspectTokenType(**data) for data
                                in Resolver.resolve_token_inspection(output)]
        else:
            token_inspection = []

        if data_extraction:
            output = CustomPipeline.execute_data_extraction(
                output,
                data_extraction
            )

        return CustomPipelineType(
            text=text,
            chosen_pre_processment=pre_processing,
            chosen_reducer=reducer,
            chosen_data_extraction=data_extraction,
            output=output,
            token_inspection=token_inspection
        )

    ##########################################################################
    # Help
    ##########################################################################
    help = graphene.List(
        graphene.String,
        language=graphene.Argument(
            enums.Language,
            description='Help Text language. Default=Pt-Br!'
        ),
        description='Returns the repository docs link!'
    )

    def resolve_help(self, info, **kwargs):
        language_options = {
            'en': 'En: For more detailed information please visit the ' \
                  'official docs page on GitHub repository!',
            'pt-br': 'Pt-Br: Para informações mais detalhadas por favor ' \
                     'consulte a documentação oficial no repositório do GitHub!'
        }
        message = language_options.get(kwargs.get('language', 'pt-br'))
        wiki_link = 'https://github.com/brunolcarli/Lisa/wiki'

        return [message, wiki_link]

    ##########################################################################
    # Versão da plataforma
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
