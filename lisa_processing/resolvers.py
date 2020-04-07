"""
Resolução dos algoritmos chamados nas queries.
"""
import itertools
import spacy
from difflib import get_close_matches as closest_token
from nltk import sent_tokenize, word_tokenize
from lisa_processing.util.nlp import (stemming, text_classifier,
                                      get_word_offense_level, remove_stopwords,
                                      remove_punctuations, get_offense_level,
                                      get_tokens_pol, is_stopword,
                                      get_word_polarity)
from lisa_processing.util.normalizer import Normalizer
from lisa_processing.util.tools import (get_entity_description,
                                        get_pos_tag_description)


SPACY = spacy.load('pt')


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
            "<class 'str'>": SPACY,
            "<class 'list'>": lemma_from_list
        }
        tokens = execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": stem_from_str,
            "<class 'list'>": stem_from_list
        }
        return execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": text_classifier,
            "<class 'list'>": classify_from_list
        }

        return execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": sent_tokenize,
            "<class 'list'>": list_sent_tokenize
        }

        return execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": word_tokenize,
            "<class 'list'>": list_tokenize
        }

        return execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": remove_sw_from_str,
            "<class 'list'>": remove_sw_from_list
        }

        return execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": remove_puncts_from_str,
            "<class 'list'>": remove_puncts_from_list
        }

        return execute.get(str(type(input_data)))(input_data)

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
            "<class 'str'>": resolve_from_str,
            "<class 'list'>": resolve_from_list
        }
        tokens = execute.get(str(type(input_data)))(input_data)
        pairs = get_word_offense_level(tokens)

        output = []
        for pair in pairs:
            # o processamento retorna o radical, ams queremos ot ermo completo
            token = closest_token(pair[0], tokens)

            # se não houver use o própprio radical
            full_token = token or pair
            output.append({
                'token': full_token[0],
                'is_offensive': bool(pair[1])
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
