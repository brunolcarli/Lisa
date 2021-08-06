r"""
   ___ __ _     _  _ ___    __ __    __    _ 
|   | (_ |_|   |_||_) |    (_ /  |_||_ |V||_|
|___|___)| |   | ||  _|_   __)\__| ||__| || |

contact info: brunolcarli@gmail.com
"""
import logging
import graphene
from django.conf import settings
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from lisa_processing import enums
from lisa_processing.resolvers import Resolver, ResolveFromDB
from lisa_processing.util.types import DynamicScalar
from lisa_processing.util.pipelines import CustomPipeline
from lisa_processing.util.nlp import stemming as stem
from lisa_processing.util.nlp import (get_word_polarity, text_classifier,
                                      get_offense_level, get_word_offense_level,
                                      is_stopword)
from lisa_processing.util.tools import (get_pos_tag_description,
                                       get_entity_description)


logger = logging.getLogger('lisa')


class TermType(graphene.ObjectType):
    """
    Padrão de resposta para processamentos de Termos armazenados no banco
    de dados.
    """
    text = graphene.String()
    part_of_speech = graphene.String()
    lemma = graphene.String()
    root = graphene.String
    polarity = graphene.Float()
    meaning = DynamicScalar()
    is_currency = graphene.Boolean()
    is_punct = graphene.Boolean()
    is_stop = graphene.Boolean()
    is_offensive = graphene.Boolean()
    is_digit = graphene.Boolean()


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
    token = graphene.String()
    entity = graphene.String()
    description = graphene.String()


class WordPolarityType(graphene.ObjectType):
    """
    Padrão de resposta para processamentos de identificação de polaridades
    de palavras.
    """
    token = graphene.String(description='Analysed token.')
    polarity = graphene.Float(description='Token polarity.')


class TextOffenseType(graphene.ObjectType):
    """
    Padrão de resposta para requisições de TextOffense.
    """
    text = graphene.String(description='Processed text!')
    average = graphene.Float(
        description='Avarage calc on based on bad words counting!'
    )
    is_offensive = graphene.Boolean(
        description='True if the sentence is offensive, False if not!'
    )


class WordOffenseType(graphene.ObjectType):
    """
    Padrão de objeto contido na lista retornada como resposta na requisição de
    processamento de wordOffenseLevel (Nível Ofensivo de palavras)
    """
    token = graphene.String(description='Analysed token.')
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


class RemoveStopWordsType(graphene.ObjectType):
    """
    Estrutura de resposta para consultas de remoção de stop words.
    """
    inputed_data = graphene.String(description='Inputed text.')
    text_output = graphene.String(description='Text without the stop words.')
    list_output = graphene.List(
        graphene.String,
        description='Token list from the processed data without the stop words.'
    )
    removed_tokens = graphene.List(
        graphene.String,
        description='Stop words removed from the inputed data.'
    )
    removed_tokens_count = graphene.Int(
        description='Number of stop words removed.'
    )

    def resolve_removed_tokens_count(self, info, **kwargs):
        return len(self.removed_tokens)


class WordTokenizeType(graphene.ObjectType):
    """
    Estrutura de resposta para consultas de tokenização.
    """
    inputed_data = graphene.String(description='Inputed text.')
    output = graphene.List(
        graphene.String,
        description='List of tokens extracted from inputed data.'
    )
    num_tokens = graphene.Int(
        description='Number of tokens found at inputed data.'
    )


class CharCounterType(graphene.ObjectType):
    """
    Estrutura de resposta para consultas de contagem de caracteres.
    """
    inputed_data = graphene.String(description='Inputed text.')
    output = graphene.List(
        graphene.String,
        description='List of chars extracted from inputed text.'
    )
    num_chars = graphene.Int(
        description='Number of chars found at inputed text.'
    )


class SentenceSegmentationType(graphene.ObjectType):
    """
    Estrutura de apresentação da fragmentação de sentenças.
    """
    inputed_data = graphene.String(description='Inputed text.')
    output = graphene.List(
        graphene.String,
        description='List of sentences extracted from inputed text.'
    )
    num_sentences = graphene.Int(description='Total sentences found in text.')


class SentimentExtractionType(graphene.ObjectType):
    """
    Estrutura de apresentação da extração de sentimento de um texto.
    """
    text = graphene.String(description='Processed text.')
    sentiment = graphene.Float(description='Extracted sentiment.')


class SentimentBatchExtractionType(graphene.ObjectType):
    """
    Estrutura de apresentação do processamento de análise de
    sentimentos sobre N entradas de texto.
    """
    count = graphene.Int(
        description='Number of texts inputed.'
    )
    positive_occurrences_count = graphene.Int(
        description='Number of positive occurrences found.'
    )
    neutral_occurrences_count = graphene.Int(
        description='Number of neutral occurrences found.'
    )
    negative_occurrences_count = graphene.Int(
        description='Number of negative occurrences found.'
    )
    positive_percentage = graphene.Float(
        description='Percentage of positive occurrences.'
    )
    neutral_percentage = graphene.Float(
        description='Percentage of neutral occurrences.'
    )
    negative_percentage = graphene.Float(
        description='Percentage of negative occurrences.'
    )
    total_sentiment = graphene.Float(
        description='Total sentiment sum extracted from all samples together.'
    )
    mean_sentiment = graphene.Float(
        description='Mean sentiment value from all samples together.'
    )
    positive_sentiments = graphene.List(
        SentimentExtractionType,
        description='List of positive occurrences and its extracted sentiment.'
    )
    neutral_sentiments = graphene.List(
        SentimentExtractionType,
        description='List of neutral occurrences and its extracted sentiment.'
    )
    negative_sentiments = graphene.List(
        SentimentExtractionType,
        description='List of negative occurrences and its extracted sentiment.'
    )

    def resolve_positive_occurrences_count(self, info, **kwargs):
        return len(self.positive_sentiments)

    def resolve_neutral_occurrences_count(self, info, **kwargs):
        return len(self.neutral_sentiments)

    def resolve_negative_occurrences_count(self, info, **kwargs):
        return len(self.negative_sentiments)

    def resolve_positive_percentage(self, info, **kwargs):
        return len(self.positive_sentiments) / self.count

    def resolve_neutral_percentage(self, info, **kwargs):
        return len(self.neutral_sentiments) / self.count

    def resolve_negative_percentage(self, info, **kwargs):
        return len(self.negative_sentiments) / self.count


class Query(graphene.ObjectType):
    """
    Queries da lisa:
        Disponibiliza as consultas de processamento de linguagem natural e
        análise de sentimentos da API.
    """

    ##########################################################################
    # SENTENCE SEGMENTATION
    ##########################################################################
    sentence_segmentation = graphene.Field(
        SentenceSegmentationType,
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
        logger.info(info.context._body.decode('utf-8'))
        sentences = Resolver.resolve_sentence_segmentation(kwargs.get('text'))
        return SentenceSegmentationType(
            inputed_data=kwargs.get('text'),
            output=sentences,
            num_sentences=len(sentences)
        )

    ##########################################################################
    # CHAR count
    ##########################################################################
    char_count = graphene.Field(
        CharCounterType,
        text=graphene.String(
            description='Input text for char segmentation count!',
            required=True
        ),
        description='Counts the number of char in the text'
    )

    def resolve_char_count(self, info, **kwargs):
        """
        Processa requisição de contagem de caracteres.
        """
        logger.info(info.context._body.decode('utf-8'))
        chars = Resolver.resolve_char_count(kwargs.get('text'))

        return CharCounterType(
            inputed_data=kwargs.get('text'),
            output=chars,
            num_chars=len(chars)
        )

    ##########################################################################
    # WORD TOKENIZE
    ##########################################################################
    word_tokenize = graphene.Field(
        WordTokenizeType,
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
        logger.info(info.context._body.decode('utf-8'))
        tokens = Resolver.resolve_tokenize(kwargs.get('text'))
        return WordTokenizeType(
            inputed_data=kwargs.get('text'),
            output=tokens,
            num_tokens=len(tokens)
        )

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
        logger.info(info.context._body.decode('utf-8'))
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
        logger.info(info.context._body.decode('utf-8'))
        return Resolver.resolve_lemming(kwargs.get('text'))

    ##########################################################################
    # STOP WORDS
    ##########################################################################
    remove_stop_words = graphene.Field(
        RemoveStopWordsType,
        text=graphene.String(
            required=True,
            description='Input text for process the stop words removal.'
        ),
        description='Remove stop words from inputed text.'
    )

    def resolve_remove_stop_words(self, info, **kwargs):
        """
        Remove as palavras vazias do texto inserido e retorna um objeto
        detalhando a operação realizada.
        """
        logger.info(info.context._body.decode('utf-8'))
        input_data = kwargs.get('text')
        resolved_data = Resolver.resolve_datailed_stopword_removal(input_data)
        return RemoveStopWordsType(inputed_data=input_data, **resolved_data)

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
        logger.info(info.context._body.decode('utf-8'))
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
        logger.info(info.context._body.decode('utf-8'))
        resolved_data = Resolver.resolve_named_entity(kwargs.get('text'))
        return [NamedEntityType(**data) for data in resolved_data]

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
    )

    def resolve_word_polarity(self, info, **kwargs):
        """
        Processa a resolução de polaridades de palavras.
        O Processamento aceita uma lista de palávras, retornando desta forma,
        uma lista de objetos contendo a palávra processada e sua polaridade.
        """
        logger.info(info.context._body.decode('utf-8'))
        resolved_data = Resolver.resolve_word_polarity(kwargs.get('word_list'))
        return [WordPolarityType(**data) for data in resolved_data]

    ##########################################################################
    # text classifier
    ##########################################################################
    sentiment_extraction = graphene.Float(
        text=graphene.String(required=True, description='Text to classify.'),
        description='Extracts text sentiment with lexical analysis.'
    )

    def resolve_sentiment_extraction(self, info, **kwargs):
        """
        Extrai o sentimento com o algoritmo léxico de Taboada, retornado do
        processamento um número de ponto flutuante entre -1 e 1 podendo
        representar a negatividade, neutralidade ou positividade
        do texto processado.
        """
        logger.info(info.context._body.decode('utf-8'))
        return Resolver.resolve_lexical_text_classifier(kwargs.get('text'))

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
        logger.info(info.context._body.decode('utf-8'))
        resolved_data = Resolver.resolve_text_offense(kwargs.get('text'))
        return TextOffenseType(text=kwargs.get('text'), **resolved_data)

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
        logger.info(info.context._body.decode('utf-8'))
        resolved_data = Resolver.resolve_word_offense(kwargs.get('word_list'))
        return [WordOffenseType(**data) for data in resolved_data]

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
        logger.info(info.context._body.decode('utf-8'))
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
        logger.info(info.context._body.decode('utf-8'))
        resolved_data = Resolver.resolve_token_inspection(kwargs.get('text'))
        return [InspectTokenType(**data) for data in resolved_data]

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
        logger.info(info.context._body.decode('utf-8'))
        return Resolver.resolve_similarity(
            kwargs.get('first_token'),
            kwargs.get('second_token')
        )

    ##########################################################################
    # Punct removal
    ##########################################################################
    remove_punctuation = graphene.List(
        graphene.String,
        text=graphene.String(
            required=True,
            description='Text to be processed.'
        ),
        description='Removes all puncts from text. Returns a list of tokens.'
    )

    def resolve_remove_punctuation(self, info, **kwargs):
        logger.info(info.context._body.decode('utf-8'))
        return Resolver.resolve_remove_puncts(kwargs.get('text'))

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
        logger.info(info.context._body.decode('utf-8'))

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
    # Sentiment Batch
    ##########################################################################
    sentiment_batch_extraction = graphene.Field(
        SentimentBatchExtractionType,
        text_list=graphene.List(
            graphene.String,
            description='List of texts for sentiment extraction!',
            required=True
        ),
        description='Extract the sentiment of each given text.'
    )

    def resolve_sentiment_batch_extraction(self, info, **kwargs):
        logger.info(info.context._body.decode('utf-8'))

        data = Resolver.resolve_sentiment_batch_extraction(kwargs['text_list'])
        return SentimentBatchExtractionType(**data)

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
        logger.info(info.context._body.decode('utf-8'))
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
        logger.info(info.context._body.decode('utf-8'))
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

    ##########################################################################
    # Termos armazenados
    ##########################################################################
    know_terms = graphene.List(
        TermType,
        description='Queries LISA know terms.',
        text__icontains=graphene.String(description='Filter by partial text.'),
        polarity__gte=graphene.Float(
            description='Filter by sentiment pol greather equal.'
        ),
        polarity__lte=graphene.Float(
            description='Filter by sentiment pol lesser equal.'
        ),
        is_stop=graphene.Boolean(description='Filter by stop words'),
        is_punct=graphene.Boolean(description='Filter by punctuations.'),
        is_digit=graphene.Boolean(description='Filter by digits.'),
        is_offensive=graphene.Boolean(description='Filter by offensive text.')
    )

    def resolve_know_terms(self, info, **kwargs):
        """
        Consulta os termos conhecidos pela LISA
        """
        logger.info(info.context._body.decode('utf-8'))
        
        return ResolveFromDB.get_terms(**kwargs)


class CreateTerm(graphene.relay.ClientIDMutation):
    """
    Registra um novo termo no banco de dados.
    """
    term = graphene.Field(TermType)

    class Input:
        text = graphene.String(required=True)
        part_of_speech = graphene.String()
        lemma = graphene.String()
        root = graphene.String()
        polarity = graphene.Float()
        meaning = DynamicScalar()
        is_currency = graphene.Boolean()
        is_digit = graphene.Boolean()
        is_punct = graphene.Boolean()
        is_stop = graphene.Boolean()
        is_offensive = graphene.Boolean()

    def mutate_and_get_payload(self, info, **kwargs):
        term = ResolveFromDB.create_term(**kwargs)    
        return CreateTerm(term)

class Mutation(object):
    create_term = CreateTerm.Field()