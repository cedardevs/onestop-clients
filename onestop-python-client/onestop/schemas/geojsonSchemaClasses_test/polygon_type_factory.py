from factory import Factory, lazy_attribute

from onestop.schemaTest2.polygon_type import PolygonType
from onestop.schemaTest2_test import fake


class PolygonTypeFactory(Factory):
    class Meta:
        model = PolygonType
    value = lazy_attribute(lambda x: fake.enum_with_schema(PolygonType))
