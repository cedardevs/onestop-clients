from factory import Factory, lazy_attribute

from onestop.schemaTest2.multi_point_type import MultiPointType
from onestop.schemaTest2_test import fake


class MultiPointTypeFactory(Factory):
    class Meta:
        model = MultiPointType
    value = lazy_attribute(lambda x: fake.enum_with_schema(MultiPointType))
