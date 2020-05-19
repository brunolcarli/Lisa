from __future__ import unicode_literals

from graphene.types.scalars import MAX_INT, MIN_INT
from graphql.language.ast import (BooleanValue, FloatValue, IntValue,
                                  ListValue, ObjectValue, StringValue)

from graphene.types.scalars import Scalar


class DynamicScalar(Scalar):
    """
    The `DynamicScalar` scalar type represents a JSON object with unknown fields

    Adapted from original type, GenericScalar
    """

    @staticmethod
    def identity(value):
        try:
            return value._asdict()
        except:
            return value

    serialize = identity
    parse_value = identity

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, (StringValue, BooleanValue)):
            return ast.value
        elif isinstance(ast, IntValue):
            num = int(ast.value)
            if MIN_INT <= num <= MAX_INT:
                return num
        elif isinstance(ast, FloatValue):
            return float(ast.value)
        elif isinstance(ast, ListValue):
            return [DynamicScalar.parse_literal(value) for value in ast.values]
        elif isinstance(ast, ObjectValue):
            return {field.name.value: DynamicScalar.parse_literal(field.value) for field in ast.fields}
        else:
            return None
