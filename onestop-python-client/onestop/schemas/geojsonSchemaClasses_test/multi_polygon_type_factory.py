from factory import Factory, lazy_attribute

from onestop.schemaTest2.multi_polygon_type import MultiPolygonType
from onestop.schemaTest2_test import fake


class MultiPolygonTypeFactory(Factory):
    class Meta:
        model = MultiPolygonType
    value = lazy_attribute(lambda x: fake.enum_with_schema(MultiPolygonType))
