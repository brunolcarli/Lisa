import graphene

import lisa_processing.schema


class Query(lisa_processing.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)