"""
   ___ __ _     _  _ ___    __ __    __    _ 
|   | (_ |_|   |_||_) |    (_ /  |_||_ |V||_|
|___|___)| |   | ||  _|_   __)\__| ||__| || |

contact info: brunolcarli@gmail.com
"""
import graphene
from nltk import sent_tokenize, word_tokenize


class Query(graphene.ObjectType):
    """
    Queries da lisa:
        Dispõe as consultas de processamentode linguagem natural e analise
        de sentimentos da API.
    """

    sentence_segmentation = graphene.List(
        graphene.String,
        text=graphene.String(
            description='Input text for sentece segmentation!',
            required=True
        ),
        description='Process a sentence segmentation over a text input.'
    )
    def resolve_sentence_segmentation(self, info, **kwargs):
        """Processa a requisição de sentence segmentation conforme RF001."""
        text = kwargs.get('text')
        segmented_text = sent_tokenize(text)

        return segmented_text

    word_tokenize = graphene.List(
        graphene.String,
        text=graphene.String(
            required=True,
            description='Text input for word tokenizing.'
        ),
        description='Process the word tokenizer request.'
    )
    def resolve_word_tokenize(self, info, **kwargs):
        """Processa requisiçõa para atomização palavras"""
        text = kwargs.get('text')
        tokenized = word_tokenize(text)

        return tokenized

    lisa = graphene.List(graphene.String)
    def resolve_lisa(self, info, **kwargs):
        """Isso é um ovo de páscoa."""
        lisa_ascii = [          
            r"      /\  /\ ",
            '  ___/  \/  \___',
            ' |              /',
            ' |             /_',
            ' /      \_| \_| /',
            '/      \/  \/  \/',
            '\   _  (o   )o  )',
            ' \ /c   \__/ --.',
            " | \_   ,     -'",
            " |_ |  '\_______)",
            '   ||      _)',
            '    |     |',
            '    OOOOOOO',
            '   /       \     ',
        ]
        return lisa_ascii
