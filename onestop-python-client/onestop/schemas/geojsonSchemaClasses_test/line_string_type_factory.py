from factory import Factory, lazy_attribute
from onestop.schemaTest2.line_string_type import LineStringType
from onestop.schemaTest2_test import fake


class LineStringTypeFactory(Factory):
    class Meta:
        model = LineStringType
    value = lazy_attribute(lambda x: fake.enum_with_schema(LineStringType))
