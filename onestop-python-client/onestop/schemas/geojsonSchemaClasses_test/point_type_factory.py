from factory import Factory, lazy_attribute

from onestop.schemaTest2.point_type import PointType
from onestop.schemaTest2_test import fake


class PointTypeFactory(Factory):
    class Meta:
        model = PointType
    value = lazy_attribute(lambda x: fake.enum_with_schema(PointType))
