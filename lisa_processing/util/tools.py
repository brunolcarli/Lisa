"""
Módulo dedicao à implementação de outras ferramentas diversas.
"""


def get_pos_tag_description(tag):
    """
    Realiza o mapeamento de uma tag padrão da etiquetação morfossintática
    (part of speech) retornando de forma explícita o equivalente em português
    para a tag recebida.

    param : tag : <str>
    return : <str>
    """
    tag_map = {
        'ADJ': 'adjetivo',
        'ADP': 'adposição',
        'ADV': 'advérbio',
        'AUX': 'verbo auxiliar',
        'CONJ': 'conjunção',
        'CCONJ': 'conjunção coordenativa',
        'DET': 'artigo',
        'INTJ': 'interjeição',
        'NOUN': 'substantivo',
        'NUM': 'numeral',
        'PART': 'partícula',
        'PRON': 'pronome',
        'PROPN': 'nome próprio',
        'PUNCT': 'pontuação',
        'SCONJ': 'conjunção subordinativa',
        'SYM': 'símbolo',
        'VERB': 'verbo',
        'X': 'outros',
        'SPACE': 'espaço'
    }

    return tag_map.get(tag, tag)


def get_entity_description(entity):
    """
    Realiza o mapeamento de uma entidade padrão da extracão de entidades
    (named entity) retornando de forma explícita o equivalente em português
    para a entidade extraída.

    param : entity : <str>
    return : <str>
    """
    ent_map = {
        'PERSON': 'pessoa',
        'PER': 'pessoa',
        'NORP': 'nacionalidade ou grupos religiosos/políticos.',
        'FAC': 'prédios, estradas, aeroportos, pontes...',
        'ORG': 'empresas, agências, instituições...',
        'GPE': 'países, cidades, estados.',
        'LOC': 'Locais sem classificação geopolitica.',
        'PRODUCT': 'objetos, veículos, alimentos...',
        'EVENT': 'batalhas, guerras, eventos esportivos...',
        'WORK_OF_ART': 'títulos de livros, canções...',
        'LAW': 'documentos nomeados que virarm leis.',
        'LANGUAGE': 'idioma',
        'DATE': 'datas ou períodos absolutos ou relativos.',
        'TIME': 'períodos de tempo menores que um dia.',
        'PERCENT': 'percentual.',
        'MONEY': 'valores monetários.',
        'QUANTITY': 'medidas.',
        'ORDINAL': 'primeiro, segundo, terceiro...',
        'CARDINAIS': 'outros numerais.'
    }

    return ent_map.get(entity, entity)
