import graphene

class Query(graphene.ObjectType):

    lisa = graphene.List(graphene.String)
    def resolve_lisa(self, info, **kwargs):
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
