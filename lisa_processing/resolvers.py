"""
Resolução dos algoritmos chamados nas queries.
"""
import logging
import itertools
import spacy
from difflib import get_close_matches as closest_token
from nltk import sent_tokenize, word_tokenize
from lisa_processing.util.nlp import (stemming, text_classifier,
                                      get_word_offense_level, remove_stopwords,
                                      remove_punctuations, get_offense_level,
                                      get_tokens_pol, is_stopword,
                                      get_word_polarity, detailed_stopword_removal)
from lisa_processing.util.normalizer import Normalizer
from lisa_processing.util.tools import (get_entity_description,
                                        get_pos_tag_description)
from lisa_processing.models import Term

logger = logging.getLogger('lisa')

logger.info('Loading Spacy...')
SPACY = spacy.load('pt')
logger.info('Done!')


class Resolver:
    """
    Classe que contém métodos resolutivos par ao processamento dos algoritmos
    utilizados pela API.
    """
    @staticmethod
    def resolve_lemming(input_data):
        """
        Resolução do processamento de lemming.

        return : <list>
        """
        normalizer = Normalizer()
        lemma_from_list = lambda texts: SPACY(normalizer.list_to_string(texts))
        execute = {
            str: SPACY,
            list: lemma_from_list
        }
        tokens = execute.get(type(input_data))(input_data)

        return [token.lemma_ for token in tokens]

    @staticmethod
    def resolve_stemming(input_data):
        """
        Resolução do processamento de stemming

        return : <list>
        """
        normalizer = Normalizer()
        stem_from_list = lambda text_list: stemming(
            Resolver.resolve_tokenize(normalizer.list_to_string(text_list))
        )
        stem_from_str = lambda text: stemming(
            Resolver.resolve_tokenize(text)
        )
        execute = {
            str: stem_from_str,
            list: stem_from_list
        }
        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_dependency_parse(input_data):
        """
        Resolução do processamento de Dependency Parsing

        param : input_data : <str> ou <list>
        return <list> de <dict>
        """
        normalizer = Normalizer()
        resolve_from_list = lambda text_list: SPACY(
            normalizer.list_to_string(text_list)
        )

        execute = {
            str: SPACY,
            list: resolve_from_list
        }

        tokens = execute.get(type(input_data))(input_data)
        result = []

        for token in tokens:
            result.append({
                'element': token.text,
                'children': [str(child) for child in token.children],
                'ancestors': [str(anc) for anc in token.ancestors]
            })

        return result

    @staticmethod
    def resolve_lexical_text_classifier(input_data):
        """
        Resolve a análise de sentimentos de um texto utilizando o
        algoritmo léxico.

        param : text : <str>
        return : <float>
        """
        normalizer = Normalizer()
        classify_from_list = lambda tokens: text_classifier(
            normalizer.list_to_string(tokens)
        )
        execute = {
            str: text_classifier,
            list: classify_from_list
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_sentence_segmentation(input_data):
        """
        Resolve a fragmentação de sentenças a partir de:
            - uma lista de textos <list>; ou
            - um texto puro (<str>)

        return : <list> : Lista de sentenças (<str>)
        """
        list_sent_tokenize = lambda sent_list: list(
            itertools.chain(*[sent_tokenize(sent) for sent in sent_list])
        )
        execute = {
            str: sent_tokenize,
            list: list_sent_tokenize
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_tokenize(input_data):
        """
        Resolve a atomização de palávras a partir de:
            - uma lista de sentenças <list>; ou
            - um texto puro (<str>)

        return : <list> : Lista de tokens (<str>)
        """
        list_tokenize = lambda texts: list(
            itertools.chain(*[word_tokenize(text) for text in texts])
        )
        execute = {
            str: word_tokenize,
            list: list_tokenize
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_remove_stopwords(input_data):
        """
        Resolve a remoção de palávras vazias a partir de:
            - uma lista de sentenças <list>; ou
            - um texto puro (<str>)

        return : <list> : Lista de tokens com significado semântico (<str>)
        """
        normalizer = Normalizer()
        remove_sw_from_str = lambda text: remove_stopwords(
            Resolver.resolve_tokenize(text)
        )
        remove_sw_from_list = lambda text_list: remove_stopwords(
            Resolver.resolve_tokenize(normalizer.list_to_string(text_list))
        )
        execute = {
            str: remove_sw_from_str,
            list: remove_sw_from_list
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_remove_puncts(input_data):
        """
        Resolve o processamento para remocão de pontuações a partir de:
            - uma lista de sentenças <list>; ou
            - um texto puro (<str>)

        return : <list> : Lista de tokens (<str>)
        """
        normalizer = Normalizer()
        remove_puncts_from_str = lambda text: remove_punctuations(
            Resolver.resolve_tokenize(text)
        )
        remove_puncts_from_list = lambda text_list: remove_punctuations(
            Resolver.resolve_tokenize(normalizer.list_to_string(text_list))
        )
        execute = {
            str: remove_puncts_from_str,
            list: remove_puncts_from_list
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_word_offense(input_data):
        """
        Resolve o processamento de identificação de palávras ofensivas.

        param : input_data : <str> or <list>
        return : <list> : Lista de <dict>
        """
        normalizer = Normalizer()
        resolve_from_list = lambda text_list: Resolver.resolve_tokenize(
            normalizer.list_to_string(text_list)
        )
        resolve_from_str = lambda text: Resolver.resolve_tokenize(text)
        execute = {
            str: resolve_from_str,
            list: resolve_from_list
        }
        tokens = execute.get(type(input_data))(input_data)
        pairs = get_word_offense_level(tokens)

        output = []
        for pair in pairs:
            # o processamento retorna o radical, ams queremos ot ermo completo
            token = closest_token(pair[0], tokens)

            # se não houver use o própprio radical
            full_token = token or pair
            output.append({
                'token': full_token[0],
                'is_offensive': bool(pair[1]),
                'value': pair[1]
            })

        return output

    @staticmethod
    def resolve_text_offense(input_data):
        """
        Resolve o processamento de classificação de um texto como ofensivo.

        param : input_data : <str> ou <list>
        return <dict>
        """
        normalizer = Normalizer()
        resolve_from_list = lambda token_list: get_offense_level(
            normalizer.list_to_string(token_list)
        )

        execute = {
            list: resolve_from_list,
            str: get_offense_level
        }

        is_offensive, average = execute.get(type(input_data))(input_data)

        return {'is_offensive': is_offensive, 'average': average}

    @staticmethod
    def resolve_word_polarity(input_data):
        """
        Resolve o processamento de polarização de palávras.

        param : input_data : <str> ou <list>
        return : <list> de <dict>
        """
        resolve_from_string = lambda text: get_tokens_pol(
            Resolver.resolve_tokenize(text)
        )

        execute = {
            str: resolve_from_string,
            list: get_tokens_pol
        }
        output = execute.get(type(input_data))(input_data)

        return output

    @staticmethod
    def resolve_named_entity(input_data):
        """
        Resolve o processamento de entidades nomeadas.

        param : input_data : <list> ou <str>
        return : <list> de <dict>
        """
        normalizer = Normalizer()

        resolve_from_string = lambda text: [{
            'token': ent.text,
            'entity': ent.label_,
            'description': get_entity_description(ent.label_)
        } for ent in SPACY(text).ents]

        resolve_from_list = lambda text_list: resolve_from_string(
            normalizer.list_to_string(text_list)
        )

        execute = {
            str: resolve_from_string,
            list: resolve_from_list
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_part_of_speech(input_data):
        """
        Resolve a marcação POS na entrada fornecida.

        param : input_data : <list> ou <str>
        return : <list> de <dict>
        """
        normalizer = Normalizer()

        resolve_from_string = lambda text: [{
            'token': token.text,
            'tag': token.pos_,
            'description': get_pos_tag_description(token.pos_)
        } for token in SPACY(text)]

        resolve_from_list = lambda text_list: resolve_from_string(
            normalizer.list_to_string(text_list)
        )

        execute = {
            str: resolve_from_string,
            list: resolve_from_list
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_token_inspection(input_data):
        """
        Resolução da inspeção de tokens.

        param : input_data : <list> ou <str>
        return : <list> de <dict>
        """
        normalizer = Normalizer()

        resolve_from_string = lambda text: [{
            'token': token.text,
            'is_alpha': token.is_alpha,
            'is_ascii': token.is_ascii,
            'is_currency': token.is_currency,
            'is_digit': token.is_digit,
            'is_punct': token.is_punct,
            'is_space': token.is_space,
            'is_stop': is_stopword(token.text),
            'lemma': token.lemma_,
            'pos_tag': get_pos_tag_description(token.pos_),
            'vector': token.vector,
            'polarity': get_word_polarity(token.text),
            'is_offensive': get_offense_level(token.text)[0],
            'root': stemming([token.text])[0]
        } for token in SPACY(text)]

        resolve_from_list = lambda text_list: resolve_from_string(
            normalizer.list_to_string(text_list)
        )

        execute = {
            str: resolve_from_string,
            list: resolve_from_list
        }

        return execute.get(type(input_data))(input_data)

    @staticmethod
    def resolve_datailed_stopword_removal(input_data):
        """
        Resolve a remoção detalhada de palávras vazias a partir de:
            - uma lista de sentenças <list>; ou
            - um texto puro (<str>)

        return : <dict> : Dicionário contendo detalhes da operação
        """
        normalizer = Normalizer()
        remove_sw_from_str = lambda text: detailed_stopword_removal(
            Resolver.resolve_tokenize(text)
        )
        remove_sw_from_list = lambda text_list: detailed_stopword_removal(
            Resolver.resolve_tokenize(normalizer.list_to_string(text_list))
        )
        execute = {
            str: remove_sw_from_str,
            list: remove_sw_from_list
        }

        return execute.get(type(input_data))(input_data)        

    @staticmethod
    def resolve_similarity(first, second):
        """
        Resolve a comparação de similaridade entre
        dois termos.
        """
        first = SPACY(first)
        second = SPACY(second)

        return first.similarity(second)

    @staticmethod
    def resolve_sentiment_batch_extraction(input_data):
        """
        Resolve a extração de sentimentos em lote.

        param : input_data : <list>
        return : <dict>
        """
        positive_sentiments = []
        negative_sentiments = []
        neutral_sentiments = []

        for data in input_data:
            extraction = {'text': data, 'sentiment': text_classifier(data)}
            if extraction['sentiment'] > 0:
                positive_sentiments.append(extraction)

            elif extraction['sentiment'] < 0:
                negative_sentiments.append(extraction)

            else:
                neutral_sentiments.append(extraction)

        # total de amostras avaliadas
        count = len(positive_sentiments) + \
                len(negative_sentiments) + \
                len(neutral_sentiments)

        # Calcula o sentimento total
        positives = [data.get('sentiment', 0) for data in positive_sentiments]
        negatives = [data.get('sentiment', 0) for data in negative_sentiments]

        # Neutros são sempre 0 então somamos apenas positivos e negativos
        total_sentiment = sum(positives + negatives)

        # A média de sentimento é a razão do total pelo número de possibilidades
        mean_sentiment = total_sentiment / count
        return {
            'count': count,
            'positive_sentiments': positive_sentiments,
            'negative_sentiments': negative_sentiments,
            'neutral_sentiments': neutral_sentiments,
            'total_sentiment': total_sentiment,
            'mean_sentiment': mean_sentiment
        }

    @staticmethod
    def resolve_char_count(input_data):
        """
        Resolve a conbtagem de caracteres.

        param : input_data : <str>
        return : <list>
        """
        return [ch for ch in input_data]


class ResolveFromDB:
    """
    Process data from local database storage.
    """

    @staticmethod
    def get_terms(**kwargs):
        """
        Read terms stored on LISA database
        """
        if not kwargs:
            return Term.objects.all()
        return Term.objects.filter(**kwargs)

    @staticmethod
    def create_term(**kwargs):
        """
        Creates a new term on the database.
        if no parameters given, default
        values will be setted.
        """
        text = kwargs['text']
        tokens = SPACY(text)

        data = {'text': text}
        if not kwargs.get('part_of_speech'):
            pos = Resolver.resolve_part_of_speech(text)[0]
            data['part_of_speech'] = f'{pos["tag"]}:{pos["description"]}'
        else:
            data['part_of_speech'] = kwargs.get('part_of_speech')

        if not kwargs.get('lemma'):
            lemma = Resolver.resolve_lemming(text)
            data['lemma'] = lemma[0]
        else:
            data['lemma'] = kwargs.get('lemma')

        if not kwargs.get('root'):
            root = Resolver.resolve_stemming(text)
            data['root'] = root[0]
        else:
            data['root'] = kwargs.get('root')

        if not kwargs.get('polarity'):
            pol = Resolver.resolve_word_polarity(text)
            data['polarity'] = pol[0].get('polarity')
        else:
            pol = kwargs.get('polarity')
            pol = -1 if pol < -1 else pol
            pol = 1 if pol > 1 else pol
            data['polarity'] = pol

        if not kwargs.get('is_currency'):
            is_currency = tokens[0].is_currency
            data['is_currency'] = is_currency
        else:
            data['is_currency'] = kwargs.get('is_currency')

        if not kwargs.get('is_punct'):
            is_punct = tokens[0].is_punct
            data['is_punct'] = is_punct
        else:
            data['is_punct'] = kwargs.get('is_punct')

        if not kwargs.get('is_stop'):
            is_stop = tokens[0].is_stop
            data['is_stop'] = is_stop
        else:
            data['i_stop'] = kwargs.get('is_stop')

        if not kwargs.get('is_digit'):
            is_digit = tokens[0].is_digit
            data['is_digit'] = is_digit
        else:
            data['is_digit'] = kwargs.get('is_digit')

        if not kwargs.get('is_offensive'):
            is_offensive = Resolver.resolve_text_offense(text)
            data['is_offensive'] = is_offensive.get('is_offensive')
        else:
            data['is_offensive'] = kwargs.get('is_offensive')

        data['meaning'] = kwargs.get('meaning')

        try:
            term = Term.objects.create(**data)
        except Exception as e:
            raise e

        return term
