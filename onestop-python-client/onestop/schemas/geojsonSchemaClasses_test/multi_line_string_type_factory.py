from factory import Factory, lazy_attribute

from onestop.schemaTest2.multi_line_string_type import MultiLineStringType
from onestop.schemaTest2_test import fake


class MultiLineStringTypeFactory(Factory):
    class Meta:
        model = MultiLineStringType
    value = lazy_attribute(lambda x: fake.enum_with_schema(MultiLineStringType))
