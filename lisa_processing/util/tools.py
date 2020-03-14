"""
Módulo dedicao à implementação de outras ferramentas diversas.
"""


def get_pos_tag_description(tag):
    """
    Realiza o mapeamento de uma tag padrão da etiquetação morfossintática
    (par of speech) retornando de forma explícita o equivalente em português
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
